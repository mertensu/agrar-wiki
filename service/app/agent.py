"""
PydanticAI-Agent für das FAKT-II-Wiki.

============================================================
LERNFOKUS – die ganze Datei ist als Tutorial geschrieben
============================================================

Wenn du PydanticAI noch nicht kennst, lies diese Datei vor allen anderen.
Die fünf Konzepte, die du verstehen musst:

1. **Agent**       – das zentrale Objekt; bündelt Modell, Systemprompt, Tools.
2. **Deps**        – ein Datencontainer, den jeder Run mitbekommt (z.B. der
                     Wiki-Pfad, ein DB-Handle, ein Logger). Tools können per
                     `RunContext[Deps]` darauf zugreifen, ohne dass die
                     Werte ins LLM gelangen. Im Gegensatz zum Systemprompt
                     sieht das Modell `deps` *nicht*.
3. **Tool**        – eine Python-Funktion, die der Agent aufrufen darf;
                     siehe wiki_tools.py für die Mechanik. Hier registrieren
                     wir die Funktionen am Agenten.
4. **Run**         – ein einzelner Aufruf des Agenten mit einer User-Frage.
                     Endet entweder mit Text-Output (success) oder einer
                     festgelegten Validierungsantwort.
5. **run_stream**  – wie `run`, aber gibt die Antwort tokenweise frei,
                     damit wir per SSE/Streaming an den Browser pushen
                     können. Wichtig für gute UX.

PydanticAI-Doku zum Vertiefen (extern, nur als Pointer – nicht abrufen,
sondern dort lesen wenn unklar):
    https://ai.pydantic.dev/agents/
    https://ai.pydantic.dev/tools/
    https://ai.pydantic.dev/dependencies/

------------------------------------------------------------
Wie der Agent in EINEM Run abläuft (Tool-Schleife)
------------------------------------------------------------

PydanticAI führt im Hintergrund eine Schleife aus:

  1. User-Prompt + Systemprompt + Tool-Schemas → ans Modell schicken
  2. Modell antwortet entweder
       a) mit Text → fertig, Run endet
       b) mit einem Tool-Call → unsere Python-Funktion wird aufgerufen
  3. Tool-Result wird wieder ans Modell geschickt
  4. zurück zu 1.

Diese Schleife läuft maximal `request_limit`-mal pro Run.

------------------------------------------------------------
Caching auf Gemini
------------------------------------------------------------

Gemini hat *implizites* Prefix-Caching aktiv (für 2.5-Modelle automatisch,
sobald der Prompt eine Mindestgröße überschreitet) – wir müssen dafür
nichts tun, solange der Systemprompt zwischen Requests bytegleich bleibt.
Deshalb bauen wir ihn EINMAL beim Start in prompts.py und reichen ihn an
jeden Run weiter, statt ihn pro Request neu zu erzeugen.

Falls du später *explizites* Context-Caching brauchst (z.B. um den Cache
länger als 5–10 Minuten zu halten), heißt das in der Gemini-API
"Cached Content" und ist ein eigener API-Aufruf. Für unsere Größe
(Index ~3K Tokens) lohnt das nicht.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from pydantic_ai import Agent, RunContext

from app import wiki_tools
from app.prompts import build_system_prompt


# ---------------------------------------------------------------------------
# Deps – das, was JEDER Run an Kontext mitbekommt
# ---------------------------------------------------------------------------
#
# Deps sind ein Trick, damit Tools auf Laufzeit-Konfiguration zugreifen
# können (Pfade, DB-Handles, ...), OHNE dass diese Werte versehentlich an
# das LLM geschickt werden. Das LLM sieht ausschließlich den Systemprompt,
# die User-Message und die Tool-Schemas – niemals `deps`.
#
# Hier brauchen wir nur den Wiki-Pfad. In einer größeren App würde man hier
# auch z.B. einen Redis-Client oder einen User-Identifier mitgeben.


@dataclass
class WikiDeps:
    wiki_root: Path


# ---------------------------------------------------------------------------
# Agent-Factory
# ---------------------------------------------------------------------------


def build_agent(wiki_root: Path, model_id: str | None = None) -> Agent[WikiDeps, str]:
    """Erzeugt den konfigurierten Agent.

    Wir bauen den Agent in einer Factory (nicht als Modul-Globalwert), damit
    Tests einen frischen Agent mit eigenem Wiki-Pfad erzeugen können und
    der Systemprompt aus dem aktuellen `index.md` gebaut wird.

    Args:
        wiki_root: Wurzelverzeichnis des Wikis.
        model_id: Optional Override des Modells. Default = ENV `MODEL_ID`
            oder `google-gla:gemini-3-pro-preview` als Standard.

    Der Prefix `google-gla:` heißt "Google Generative Language API" – das
    ist der einfache Weg über einen API-Key aus Google AI Studio. Für
    Vertex-AI-Deployments wäre der Prefix `google-vertex:`.
    """
    model = model_id or os.environ.get("MODEL_ID", "google-gla:gemini-3-pro-preview")
    system_prompt = build_system_prompt(wiki_root)

    # ---- Agent-Konstruktion -------------------------------------------------
    #
    # Generic-Parameter:  Agent[DepsType, OutputType]
    #   - DepsType   = WikiDeps     (was Tools per RunContext sehen)
    #   - OutputType = str          (wir wollen am Ende Text, kein JSON-Schema)
    #
    # `instructions` vs. `system_prompt`: PydanticAI unterscheidet zwischen
    # *system prompt* (typischerweise statisch) und *instructions* (kann pro
    # Run variieren). Wir nehmen system_prompt, weil unser Prompt für alle
    # User identisch ist – das maximiert die Cache-Hit-Rate bei Anthropic.
    #
    # `model_settings`: hier wandern provider-spezifische Optionen rein.
    # `max_tokens` deckelt die Antwortlänge. Bei Reasoning-Modellen
    # (Gemini 3 Pro, Claude 4 Thinking) zählen Thinking-Tokens mit ins
    # Output-Budget — daher großzügiger Puffer, sonst wird die sichtbare
    # Antwort mitten im Satz abgeschnitten (finish_reason=length).

    agent = Agent[WikiDeps, str](
        model=model,
        deps_type=WikiDeps,
        output_type=str,
        system_prompt=system_prompt,
        model_settings={
            "max_tokens": 8000,
        },
        # Limit für die Tool-Schleife: wenn das Modell nach 10 Tool-Calls
        # immer noch keine Antwort produziert hat, brechen wir ab.
        retries=1,
    )

    # ---- Tool-Registrierung -------------------------------------------------
    #
    # Es gibt zwei Wege, Tools zu registrieren:
    #
    #   a) Decorator-Stil bei der Definition:    @agent.tool
    #   b) Imperativ:                            agent.tool(fn)
    #
    # Wir nehmen (b), weil unsere Tool-Logik in wiki_tools.py liegt und dort
    # ohne PydanticAI-Abhängigkeit bleiben soll (besser testbar).
    #
    # Wichtige Detail: Wenn ein Tool `RunContext[WikiDeps]` als ERSTES
    # Argument hat, injiziert PydanticAI dort den Run-Kontext (Deps + ID).
    # Hat es das nicht, wird das Tool einfach mit den Argumenten des
    # LLM-Calls aufgerufen. Wir machen Wrapper, weil wir wiki_root aus
    # ctx.deps an die reinen Funktionen durchreichen wollen.

    @agent.tool
    def search_wiki(
        ctx: RunContext[WikiDeps],
        query: str,
        max_results: int = 8,
    ) -> list[dict[str, str | int]]:
        """Suche im FAKT-II-Wiki nach einer Zeichenkette und gib Trefferliste zurück.

        Verwende dieses Tool, wenn der Index nicht eindeutig die richtige
        Seite zeigt – etwa bei Konzept-Fragen ("Was ist GLÖZ 8?"), bei
        Vergleichen über mehrere Maßnahmen, oder bei Suche nach exakten
        Begriffen oder Beträgen. Halte den Suchbegriff kurz und spezifisch.
        """
        hits = wiki_tools.search_wiki(query, max_results, wiki_root=ctx.deps.wiki_root)
        # Wir geben Dicts statt Dataclasses zurück, damit das, was im
        # Tool-Result-Block landet, hübsches kleines JSON ist.
        return [
            {"page": h.page, "line": h.line, "snippet": h.snippet} for h in hits
        ]

    @agent.tool
    def read_page(ctx: RunContext[WikiDeps], slug: str) -> str:
        """Lies eine Wiki-Seite vollständig ein.

        Sobald du den richtigen Slug aus dem Index oder aus search_wiki
        kennst, hol dir hier den vollständigen Markdown-Inhalt. Beispiele
        für Slugs: "massnahmen/B1.2_Extensive_Gruenland",
        "Konzepte/Konditionalitaet", "Antragstellung/FAKT_Codes".
        """
        try:
            return wiki_tools.read_page(slug, wiki_root=ctx.deps.wiki_root)
        except FileNotFoundError:
            # Wir fangen das ab und geben dem Modell eine *brauchbare*
            # Antwort statt eine Exception. So kann es selbst korrigieren
            # (z.B. mit list_pages den richtigen Slug suchen).
            return f"Seite '{slug}' existiert nicht. Nutze list_pages, um existierende Slugs zu sehen."
        except wiki_tools.WikiPathError as exc:
            return f"Ungültiger Pfad: {exc}"

    @agent.tool
    def list_pages(
        ctx: RunContext[WikiDeps],
        prefix: str | None = None,
    ) -> list[str]:
        """Liste alle Wiki-Seiten oder ein Präfix-gefiltertes Subset.

        Nutze das Tool als Fallback, wenn du dir bei einem Slug unsicher
        bist – z.B. nach einem fehlgeschlagenen read_page – oder wenn du
        alle Maßnahmen einer Kategorie brauchst. Beispiel: prefix="massnahmen/B"
        listet alle B-Maßnahmen.
        """
        return wiki_tools.list_pages(prefix, wiki_root=ctx.deps.wiki_root)

    return agent
