"""
Wiki-Tools – die Funktionen, die der LLM-Agent aufrufen darf.

============================================================
LERNFOKUS: Was sind "Tools" in PydanticAI eigentlich?
============================================================

Ein "Tool" ist nichts anderes als eine **Python-Funktion**, die der Agent
während eines Runs aufrufen darf. PydanticAI macht aus jeder solchen Funktion
automatisch ein JSON-Schema, das dem LLM mitgeschickt wird – das LLM sieht
dann ungefähr:

    Tool: search_wiki
    Description: <docstring>
    Parameters: { query: str, max_results: int = 8 }

Wichtige Konsequenzen daraus:

1.  **Der Docstring ist nicht nur Doku, er ist Prompt.**
    Was hier steht, wird dem Modell wortwörtlich als Tool-Beschreibung
    serviert. Schreibe also so, dass das Modell versteht, wann es das
    Tool aufrufen soll – nicht so, wie man Kollegen Code dokumentiert.

2.  **Type-Hints sind verbindlich.**
    Aus `query: str, max_results: int = 8` baut PydanticAI ein Schema mit
    Pflichtfeld `query` und Optional-Feld `max_results`. Falsche Typen
    werden vor dem Aufruf vom Pydantic-Validator abgefangen, das LLM kann
    keinen kaputten Aufruf erzwingen.

3.  **Returns gehen direkt zurück ans Modell.**
    Was die Funktion returnt, wird (als Text/JSON) wieder Teil des Modell-
    Kontexts – als "tool_result"-Block. Das nächste Modell-Output darauf
    sieht dann genau das, was hier zurückkommt. Halte Returns daher
    knapp und strukturiert; lange Roh-Dumps fluten den Kontext.

Die Tools werden in `agent.py` registriert (siehe dort), nicht hier.
Hier liegen nur die reinen Funktionen + Hilfen, damit die Logik unabhängig
testbar ist.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

# Wiki-Wurzel: Wir setzen die so, dass sie aus Sicht des laufenden Containers
# stimmt (im Docker liegt das Wiki unter /app/wiki). Lokal kann der Aufrufer
# die Variable WIKI_ROOT überschreiben (siehe main.py).
DEFAULT_WIKI_ROOT = Path(__file__).resolve().parents[2] / "wiki"


# Pfad-Präfixe (relativ zu wiki/), die der Agent NICHT sehen soll.
# Anwendungsfall: Test-Mode. Wenn man prüfen will, ob die Antwort aus Primitiven
# (Maßnahmen-/Konzept-Seiten) rekonstruiert wird, statt aus einer vorgekochten
# Beispielfrage paraphrasiert. Setze z.B.:
#     WIKI_EXCLUDE_PREFIXES=Beispielfragen,_archive
# Wirkt auf search_wiki, read_page, list_pages, build_directory_overview und
# load_index. Wiki-Dateien bleiben unverändert auf der Platte.
EXCLUDE_PREFIXES: tuple[str, ...] = tuple(
    p.strip().rstrip("/")
    for p in os.environ.get("WIKI_EXCLUDE_PREFIXES", "").split(",")
    if p.strip()
)


def _is_excluded(slug_or_relpath: str) -> bool:
    """True, wenn der Slug/Pfad mit einem konfigurierten Exclude-Präfix beginnt."""
    if not EXCLUDE_PREFIXES:
        return False
    s = slug_or_relpath.lstrip("/")
    return any(s == p or s.startswith(p + "/") for p in EXCLUDE_PREFIXES)


@dataclass(frozen=True)
class SearchHit:
    """Ein Treffer aus search_wiki – kompakt, weil das alles in den Prompt zurück fließt."""

    page: str  # Slug ohne .md, z.B. "massnahmen/B1.2_Extensive_Gruenland"
    line: int
    snippet: str

    def to_text(self) -> str:
        return f"{self.page}:{self.line}  {self.snippet}"


def _resolve_wiki_root(root: Path | None = None) -> Path:
    return (root or DEFAULT_WIKI_ROOT).resolve()


# ---------------------------------------------------------------------------
# search_wiki
# ---------------------------------------------------------------------------

# Wir lassen ripgrep die Arbeit machen, statt selbst durch alle Dateien zu
# laufen. Das ist um Größenordnungen schneller und gibt uns Zeilen-genaue
# Treffer "umsonst". Falls rg nicht verfügbar ist, fallen wir auf eine
# einfache Python-Suche zurück (für Tests / lokale Umgebungen ohne rg).
def _ripgrep_available() -> bool:
    try:
        subprocess.run(
            ["rg", "--version"], check=True, capture_output=True, timeout=2
        )
        return True
    except (FileNotFoundError, subprocess.SubprocessError):
        return False


def search_wiki(
    query: str,
    max_results: int = 12,
    *,
    wiki_root: Path | None = None,
    per_file_cap: int = 2,
) -> list[SearchHit]:
    """Suche eine Zeichenkette im Wiki und gib Treffer mit Datei + Zeile zurück.

    Verwende dieses Tool, wenn das Inhaltsverzeichnis (`index.md`) keinen klaren
    Treffer liefert – z.B. bei Fragen zu Konzepten ("Was bedeutet GLÖZ 8?"), zu
    Förderdetails, die in mehreren Maßnahmen-Seiten erwähnt sind, oder wenn der
    User einen exakten Begriff oder eine Zahl sucht. Die Suche ist literal
    (keine Regex), case-insensitive.

    Pro Datei werden höchstens `per_file_cap` Treffer ins Ergebnis aufgenommen,
    damit eine einzelne Tabellenseite (z.B. Nutzcodeliste) nicht das ganze
    Trefferbudget aufbraucht und die eigentlich relevante Maßnahmenseite nie
    erscheint.

    Args:
        query: Suchbegriff. Halte ihn präzise (1–4 Wörter); zu kurze Queries
            wie "Förder" liefern hunderte Treffer und blähen den Kontext auf.
        max_results: Maximale Anzahl an Treffern (default 12).
        per_file_cap: Höchstzahl an Treffern pro Datei (default 2).

    Returns:
        Liste von SearchHit – jeder Treffer enthält Seiten-Slug, Zeilennummer
        und einen kurzen Snippet. Leer, wenn nichts gefunden wurde.
    """
    if not query or not query.strip():
        return []
    max_results = max(1, min(max_results, 25))
    per_file_cap = max(1, per_file_cap)
    root = _resolve_wiki_root(wiki_root)

    if _ripgrep_available():
        # rg-Optionen: -n Zeilennummern, -i case-insensitive, -F literal
        # (kein Regex), --no-heading damit jede Zeile self-contained ist.
        # --max-count begrenzt rg-seitig pro Datei, wir filtern zusätzlich.
        proc = subprocess.run(
            [
                "rg",
                "-n",
                "-i",
                "-F",
                "--no-heading",
                "--max-count",
                str(per_file_cap),
                "--",
                query,
                str(root),
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        raw = proc.stdout
    else:
        raw = _python_grep(query, root, max_results, per_file_cap)

    hits: list[SearchHit] = []
    per_file: dict[str, int] = {}
    for line in raw.splitlines():
        # rg-Format: <pfad>:<zeile>:<inhalt>
        m = re.match(r"^(.+?\.md):(\d+):(.*)$", line)
        if not m:
            continue
        path, lineno, content = m.groups()
        try:
            rel = Path(path).resolve().relative_to(root)
        except ValueError:
            continue
        slug = rel.with_suffix("").as_posix()
        if _is_excluded(slug):
            continue
        if per_file.get(slug, 0) >= per_file_cap:
            continue
        snippet = content.strip()
        if len(snippet) > 200:
            snippet = snippet[:197] + "..."
        hits.append(SearchHit(page=slug, line=int(lineno), snippet=snippet))
        per_file[slug] = per_file.get(slug, 0) + 1
        if len(hits) >= max_results:
            break
    return hits


def _python_grep(
    query: str, root: Path, max_results: int, per_file_cap: int
) -> str:
    """Reiner Python-Fallback, falls ripgrep im Container nicht installiert ist."""
    needle = query.lower()
    out: list[str] = []
    for md in root.rglob("*.md"):
        rel = md.relative_to(root).as_posix()
        if _is_excluded(rel):
            continue
        try:
            file_hits = 0
            for i, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                if needle in line.lower():
                    out.append(f"{md}:{i}:{line}")
                    file_hits += 1
                    if file_hits >= per_file_cap:
                        break
                    if len(out) >= max_results * 3:
                        return "\n".join(out)
        except (OSError, UnicodeDecodeError):
            continue
    return "\n".join(out)


# ---------------------------------------------------------------------------
# read_page
# ---------------------------------------------------------------------------


class WikiPathError(ValueError):
    """Ungültiger oder gefährlicher Pfad – z.B. Path-Traversal-Versuch."""


def _safe_resolve(slug: str, root: Path) -> Path:
    """Mappt einen Slug auf einen tatsächlichen Pfad – mit Traversal-Schutz.

    Erlaubt sind nur Pfade, die nach Auflösung (Symlinks, '..' etc.) immer
    noch unterhalb von `root` liegen. Damit kann das LLM auch durch einen
    Trick wie '../../etc/passwd' nichts außerhalb des Wikis lesen.
    """
    if not slug or slug.startswith("/") or "\x00" in slug:
        raise WikiPathError(f"Ungültiger Slug: {slug!r}")
    # Wir sind tolerant gegenüber '.md'-Suffix; das Modell schickt mal mit, mal ohne.
    candidate = (root / slug).with_suffix(".md")
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root):
        raise WikiPathError(f"Pfad außerhalb des Wikis: {slug!r}")
    return resolved


class WikiAmbiguousSlugError(FileNotFoundError):
    """Slug matcht mehrere Dateien — Modell muss präziser werden."""

    def __init__(self, slug: str, candidates: list[str]):
        self.slug = slug
        self.candidates = candidates
        super().__init__(
            f"Slug '{slug}' ist mehrdeutig. Kandidaten: {', '.join(candidates)}. "
            f"Ruf read_page mit dem vollen Pfad auf, z.B. '{candidates[0]}'."
        )


def _fuzzy_lookup(slug: str, root: Path) -> Path | None:
    """Wenn der direkte Pfad nicht existiert, suche nach Basename im ganzen Wiki.

    Inspiriert vom Obsidian-Wikilink-Verhalten: '[[E7_Bluehflaechen]]' wird
    Obsidian-seitig auf wiki/massnahmen/E7_Bluehflaechen.md aufgelöst, ohne
    dass das Verzeichnis explizit angegeben werden muss. Wir machen dasselbe.

    Returnt:
        - Path, wenn genau eine Datei matcht.
        - None, wenn keine Datei matcht (Caller wirft FileNotFoundError).
    Raises:
        WikiAmbiguousSlugError, wenn mehrere Dateien matchen.
    """
    # Letzte Pfadkomponente, ohne .md
    basename = slug.rsplit("/", 1)[-1]
    if basename.endswith(".md"):
        basename = basename[:-3]
    matches = list(root.rglob(f"{basename}.md"))
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        slugs = sorted(
            m.relative_to(root).with_suffix("").as_posix() for m in matches
        )
        raise WikiAmbiguousSlugError(slug, slugs)
    return None


def _suggest_similar(slug: str, root: Path, limit: int = 5) -> list[str]:
    """Findet Slugs, die ähnlich aussehen — als Hilfe für die Fehlermeldung."""
    import difflib

    basename = slug.rsplit("/", 1)[-1].removesuffix(".md").lower()
    all_slugs = [
        s for md in root.rglob("*.md")
        if not _is_excluded((s := md.relative_to(root).with_suffix("").as_posix()))
    ]
    # difflib gibt die besten n Treffer nach Ähnlichkeit zurück.
    return difflib.get_close_matches(
        basename, [s.rsplit("/", 1)[-1].lower() for s in all_slugs], n=limit, cutoff=0.5
    )[:limit] or all_slugs[:limit]


def read_page(slug: str, *, wiki_root: Path | None = None) -> str:
    """Lies eine einzelne Wiki-Seite vollständig ein.

    Rufe dieses Tool auf, sobald du aus dem Index oder aus search_wiki einen
    Slug gefunden hast und den vollen Inhalt brauchst, um die Frage zu
    beantworten.

    Slug-Formate, die alle funktionieren:
        "massnahmen/B1.2_Extensive_Gruenland"   (voller Pfad)
        "B1.2_Extensive_Gruenland"              (nur Basename — Tool findet die Datei)
        "Konzepte/Konditionalitaet"
        "index"

    Wenn der Slug ohne Verzeichnis kommt (Obsidian-Wikilink-Stil), löst das
    Tool den vollen Pfad selbst auf, sofern der Basename eindeutig ist.

    Args:
        slug: Pfad oder Basename innerhalb des Wikis ohne .md-Endung.
            Keine '..', keine absoluten Pfade.

    Returns:
        Roher Markdown-Inhalt der Seite (inkl. YAML-Frontmatter).

    Raises:
        FileNotFoundError: Wenn die Seite nicht existiert; Fehlermeldung
            enthält dann ähnliche Slug-Kandidaten zur Selbstkorrektur.
        WikiAmbiguousSlugError (FileNotFoundError-Subklasse): Wenn der
            Basename mehrdeutig ist; Fehlermeldung enthält die Kandidaten.
    """
    root = _resolve_wiki_root(wiki_root)
    path = _safe_resolve(slug, root)

    def _check_excluded(p: Path) -> None:
        rel = p.relative_to(root).as_posix()
        if _is_excluded(rel):
            raise FileNotFoundError(
                f"Wiki-Seite '{slug}' nicht gefunden. "
                f"Volle Liste: list_pages()."
            )

    if path.is_file():
        _check_excluded(path)
        return path.read_text(encoding="utf-8")
    # Direkter Pfad nicht da → Fuzzy-Auflösung über den Basename versuchen.
    fuzzy = _fuzzy_lookup(slug, root)
    if fuzzy is not None:
        _check_excluded(fuzzy)
        return fuzzy.read_text(encoding="utf-8")
    candidates = _suggest_similar(slug, root)
    raise FileNotFoundError(
        f"Wiki-Seite '{slug}' nicht gefunden. Ähnliche Slugs: "
        f"{', '.join(candidates) if candidates else '(keine ähnlichen)'}. "
        f"Volle Liste: list_pages()."
    )


# ---------------------------------------------------------------------------
# list_pages
# ---------------------------------------------------------------------------


def list_pages(
    prefix: str | None = None,
    *,
    wiki_root: Path | None = None,
) -> list[str]:
    """Liste verfügbare Wiki-Seiten auf, optional gefiltert nach Pfadpräfix.

    Verwende das Tool als Fallback, wenn du dir bei einem Slug unsicher bist
    – etwa wenn read_page einen FileNotFoundError wirft – oder wenn du alle
    Maßnahmen einer Kategorie sehen möchtest (z.B. prefix="massnahmen/B").

    Args:
        prefix: Optional. Nur Slugs zurückgeben, die mit diesem Präfix
            beginnen. None = alle Seiten.

    Returns:
        Sortierte Liste von Slugs (ohne .md). Maximal 200 Einträge, damit
        wir den Kontext nicht fluten.
    """
    root = _resolve_wiki_root(wiki_root)
    out: list[str] = []
    for md in root.rglob("*.md"):
        slug = md.relative_to(root).with_suffix("").as_posix()
        if _is_excluded(slug):
            continue
        if prefix and not slug.startswith(prefix):
            continue
        out.append(slug)
    out.sort()
    return out[:200]


def load_index(*, wiki_root: Path | None = None) -> str:
    """Liest `wiki/index.md` einmalig (für Systemprompt-Einbettung).

    Wenn EXCLUDE_PREFIXES gesetzt ist, werden Bullets aus dem Index entfernt,
    deren `[[...]]`-Wikilink auf eine ausgeschlossene Seite zeigt — und
    Section-Header (`## ...`), deren Bullets dadurch komplett verschwinden,
    werden ebenfalls entfernt. Damit "weiß" der Agent gar nicht, dass es
    z.B. Beispielfragen gibt.
    """
    root = _resolve_wiki_root(wiki_root)
    text = (root / "index.md").read_text(encoding="utf-8")
    if not EXCLUDE_PREFIXES:
        return text

    wikilink_re = re.compile(r"\[\[([^\]\|\\]+)")
    all_slugs = {
        md.relative_to(root).with_suffix("").as_posix() for md in root.rglob("*.md")
    }

    def link_excluded(line: str) -> bool:
        m = wikilink_re.search(line)
        if not m:
            return False
        target = m.group(1).rstrip("\\").split("#", 1)[0]
        # Direkter Pfad-Match
        if _is_excluded(target):
            return True
        # Basename-only Wikilink: über vollständige Slug-Liste auflösen
        if "/" not in target:
            for s in all_slugs:
                if s.rsplit("/", 1)[-1] == target and _is_excluded(s):
                    return True
        return False

    # Pass 1: Bullet-Zeilen mit ausgeschlossenen Wikilinks entfernen.
    kept_lines = [ln for ln in text.splitlines() if not link_excluded(ln)]

    # Pass 2: Section-Header ohne verbleibende Bullets droppen.
    # Eine "leere" Section ist `## Foo` gefolgt nur von Leerzeilen bis zum
    # nächsten `## ` oder Dateiende.
    out: list[str] = []
    i = 0
    while i < len(kept_lines):
        line = kept_lines[i]
        if line.startswith("## "):
            j = i + 1
            has_content = False
            while j < len(kept_lines) and not kept_lines[j].startswith("## "):
                if kept_lines[j].strip() and not kept_lines[j].startswith("#"):
                    has_content = True
                j += 1
            if has_content:
                out.append(line)
                out.extend(kept_lines[i + 1 : j])
            i = j
        else:
            out.append(line)
            i += 1
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Verzeichnisstruktur-Übersicht (für Systemprompt)
# ---------------------------------------------------------------------------
#
# Pro Top-Level-Verzeichnis im Wiki ein erklärender Eintrag, plus die Anzahl
# der Seiten. Erklärungen sind hier zentral konfiguriert, damit das Modell
# weiß, wozu jeder Ordner da ist — ohne dass wir die Liste aller 95 Slugs
# in den Prompt dumpen müssen (Token-sparsam).
_DIR_DESCRIPTIONS: dict[str, str] = {
    "massnahmen": "eine Seite pro FAKT-Maßnahme (Slug = Code_Name, z.B. B1.2_Extensive_Gruenland)",
    "Konzepte": "Schlüsselbegriffe (Konditionalitaet, RGV, Oeko-Regelungen, GLOEZ_*, GAB_* etc.)",
    "Antragstellung": "Checklisten und Hinweise zur Antragstellung, thematisch gruppiert",
    "Kategorien": "Übersichtsseiten je Kategorie A–G (Massnahmen-Listen)",
    "Beispielfragen": "Vorgefilterte Antworten zu typischen Beraterfragen",
    "strategie": "Strategieseiten (z.B. wie wähle ich die richtige Maßnahmenkombination)",
}


def build_directory_overview(*, wiki_root: Path | None = None) -> str:
    """Baut eine kompakte Verzeichnis-Übersicht für den Systemprompt.

    Format pro Zeile:
        - <ordner>/<beispiel-slug>   (<n> Seiten — <Beschreibung>)

    Plus Top-Level-Seiten (z.B. index, FAKT_II_Uebersicht), die direkt unter
    wiki/ liegen.
    """
    root = _resolve_wiki_root(wiki_root)
    lines: list[str] = []

    # Unterordner mit Beschreibung
    subdirs: dict[str, list[str]] = {}
    toplevel: list[str] = []
    for md in root.rglob("*.md"):
        rel = md.relative_to(root)
        parts = rel.parts
        if parts[0].startswith("_"):  # _archive etc. überspringen
            continue
        slug = rel.with_suffix("").as_posix()
        if _is_excluded(slug):
            continue
        if len(parts) == 1:
            toplevel.append(slug)
        else:
            subdirs.setdefault(parts[0], []).append(slug)

    for d in sorted(subdirs):
        slugs = sorted(subdirs[d])
        desc = _DIR_DESCRIPTIONS.get(d, "")
        example = slugs[0] if slugs else f"{d}/..."
        line = f"  - {d}/  ({len(slugs)} Seiten"
        if desc:
            line += f" — {desc}"
        line += f")\n      Beispiel-Slug: {example}"
        lines.append(line)

    if toplevel:
        lines.append(
            "  - <Top-Level>  (direkt unter wiki/, kein Verzeichnis-Präfix nötig)\n"
            f"      Seiten: {', '.join(sorted(toplevel))}"
        )

    return "\n".join(lines)
