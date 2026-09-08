# LangChain/LangGraph vs. PydanticAI — Lernnotizen

Konsolidierte Notizen aus dem Gespräch: was die beiden Frameworks unterscheidet,
wo sie sich entsprechen, und wie man die typischen LangGraph-Patterns in
PydanticAI ausdrückt.

---

## 1. Das mentale Modell

**LangChain** ist ein Ökosystem, das in mehrere Schichten zerfällt:

- `langchain-core` — Messages, Models, Tools (Basis-Bausteine)
- `langgraph` — Workflow-Layer mit State, Nodes, Edges (das, was "Agent-Building" eigentlich macht)
- `langsmith` — Observability
- `langserve` — FastAPI-Wrapper für HTTP-Bereitstellung
- `langgraph cloud` — Managed Deployment

**PydanticAI** ist gezielt schmaler:

- `Agent` mit Tools, Deps, System-Prompt, Output-Type
- Kein Graph-Layer — der Tool-Loop ist Framework-intern
- Provider-Wechsel über String (`"google-gla:..."`, `"anthropic:..."`)
- Logfire (von Pydantic) als Observability
- Für HTTP: bring your own FastAPI

Philosophisch:

- **LangGraph:** "alles ist ein Graph". Du baust die Kontrollflüsse explizit als
  State Machine. Mehr Scaffolding, dafür inspizierbar und flexibel.
- **PydanticAI:** "alles ist eine typisierte Funktion". Loop ist implizit.
  Weniger Code, dafür Flexibilität auf "Standard-Loop" begrenzt.

---

## 2. Komponenten-Mapping

| Anliegen | Current Stack (FAKT) | LangChain-Welt |
|---|---|---|
| Web-Server | FastAPI | FastAPI (oder LangServe-Wrapper) |
| Agent-Framework | PydanticAI | langchain-core + LangGraph |
| Provider-Abstraktion | String `"google-gla:..."` | Klasse pro Provider (`ChatGoogleGenerativeAI(...)`) |
| Tool-Definition | `@agent.tool` + Type-Hints | `@tool` Decorator oder `BaseTool`-Subklasse |
| Deps an Tools durchreichen | `RunContext[Deps]` als erstes Arg | `RunnableConfig` / `configurable` |
| Strukturierter Output | `output_type=PydanticModel` | `with_structured_output(...)` |
| Konversations-Historie | `result.all_messages()` | `MessagesState` mit `add_messages`-Reducer |
| Tool-Loop / Routing | implizit im `Agent` | StateGraph mit Conditional Edges |
| Streaming | `agent.run_stream` + `stream_text(delta=True)` | `.astream(...)` mit Event-Typen |
| Tracing | Logfire | LangSmith |
| Deployment | Docker beliebig | Docker oder LangGraph Cloud |

**FastAPI hat keinen LangChain-Ersatz** — auch wer LangGraph nimmt, serviert
es typischerweise hinter FastAPI/LangServe.

---

## 3. Ein einfacher Agent im Vergleich

### LangGraph

```python
from langgraph.graph import StateGraph, END, MessagesState
from langgraph.prebuilt import ToolNode

def call_model(state):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state):
    last_msg = state["messages"][-1]
    return "tools" if last_msg.tool_calls else END

graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)
graph.add_node("tools", ToolNode([my_tool]))
graph.set_entry_point("agent")
graph.add_conditional_edges("agent", should_continue)
graph.add_edge("tools", "agent")   # ← der Tool-Loop

app = graph.compile()
result = app.invoke({"messages": [HumanMessage("Frage")]})
```

### PydanticAI

```python
from pydantic_ai import Agent, RunContext

agent = Agent[Deps, str](
    model="google-gla:gemini-3-pro-preview",
    deps_type=Deps,
    output_type=str,
    system_prompt="...",
)

@agent.tool
def my_tool(ctx: RunContext[Deps], x: str) -> str:
    """Docstring landet als Tool-Description beim LLM."""
    return do_work(x, ctx.deps)

result = await agent.run("Frage", deps=Deps(...))
```

Der Tool-Loop ist in PydanticAI **nicht im User-Code sichtbar** — er ist
Framework-intern. Genau die Kante `tools → agent` in LangGraph entspricht
ihm.

---

## 4. State Reducers in LangGraph — wofür der Aufwand?

In LangGraph muss man für Listen-State einen Reducer angeben, sonst überschreiben
parallele Updates einander:

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    #         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    #         "Append statt Überschreiben"
```

Reducer sind die Eintrittskarte für drei Fähigkeiten:

1. **Parallele Knoten** — fan-out auf mehrere Suchagenten, fan-in mit Merge.
2. **Checkpointing** — State nach jedem Schritt persistieren, Crash-Resume.
3. **Time-Travel** — an einem alten Checkpoint einsteigen, Alternativen testen.

**Trade-off:**
- Brauchst du das? → Aufwand zahlt sich aus.
- Brauchst du es nicht? → Pure Overhead für simple Agenten.

PydanticAI hat kein Reducer-Konzept. Wer Parallelität braucht, nimmt
`asyncio.gather` und führt die Ergebnisse selbst zusammen.

---

## 5. Multi-Agent in PydanticAI — drei Muster

PydanticAI hat kein Graph-Konstrukt. Multi-Agent wird in Python orchestriert:

| Muster | Wann | Wer entscheidet |
|---|---|---|
| Agent-as-Tool | Supervisor mit Spezialisten | Das LLM des Supervisors |
| Programmatische Pipeline | Fixe Reihenfolge / parallele Schritte | Du, in Python |
| Handoff via `message_history` | Konversation weiterreichen | Du, mit Kontextweitergabe |

### Muster A: Agent-as-Tool

Ein Agent ruft einen anderen Agent als Tool auf. Aus Sicht des Supervisor-LLMs
ist es einfach ein Tool — was hinter dem Tool steckt, weiß es nicht.

```python
rules_agent = Agent[Deps, str](
    model="google-gla:gemini-2.5-flash",  # billig
    deps_type=Deps,
    system_prompt="Du bist Regel-Experte ...",
)

@rules_agent.tool
def read_wiki_page(ctx: RunContext[Deps], slug: str) -> str:
    return (ctx.deps.wiki_root / f"{slug}.md").read_text()

calc_agent = Agent[None, str](
    model="google-gla:gemini-2.5-flash",
    system_prompt="Du rechnest Förderbeträge aus ...",
)

supervisor = Agent[Deps, str](
    model="google-gla:gemini-3-pro-preview",   # gut im Synthetisieren
    deps_type=Deps,
    system_prompt="Du koordinierst Spezialisten ...",
)

@supervisor.tool
async def frage_regelexperte(ctx: RunContext[Deps], frage: str) -> str:
    """Für FAKT-Auflagen und Fördersätze."""
    result = await rules_agent.run(frage, deps=ctx.deps)
    return result.output

@supervisor.tool
async def frage_rechner(satz_eur_pro_ha: float, flaeche_ha: float) -> str:
    """Konkreten Förderbetrag ausrechnen."""
    prompt = f"Satz: {satz_eur_pro_ha} €/ha, Fläche: {flaeche_ha} ha."
    result = await calc_agent.run(prompt)
    return result.output

result = await supervisor.run("Lohnt sich B1.2 auf 8 ha?", deps=Deps(...))
```

Drei LLM-Calls in einer logischen "Konversation" für den User. Verschiedene
Modelle pro Agent (Flash für Lookup, Pro für Synthese) — bewährte
Kosten-Optimierung.

### Muster B: Programmatische Pipeline

Fix vorgegebene Reihenfolge — kein Grund, das LLM entscheiden zu lassen:

```python
async def beraten(frage: str, deps: Deps) -> str:
    regeln = await rules_agent.run(frage, deps=deps)
    final = await supervisor.run(
        f"Frage: {frage}\n\nRegeln:\n{regeln.output}",
        deps=deps,
    )
    return final.output
```

Parallel statt sequenziell — das LangGraph-Reducer-Pendant:

```python
import asyncio

async def beraten_parallel(frage: str, deps: Deps) -> str:
    regeln_task = rules_agent.run("Auflagen: " + frage, deps=deps)
    nachbarn_task = nachbar_agent.run("Alternativen: " + frage, deps=deps)

    regeln, nachbarn = await asyncio.gather(regeln_task, nachbarn_task)

    return (await supervisor.run(
        f"Frage: {frage}\nRegeln: {regeln.output}\nAlt: {nachbarn.output}",
        deps=deps,
    )).output
```

### Muster C: Handoff mit Konversations-Historie

```python
async def triage_dann_fach(frage: str, deps: Deps) -> str:
    triage = await triage_agent.run(frage, deps=deps)
    fach = await fach_agent.run(
        "Bitte übernimm",
        message_history=triage.all_messages(),   # ← der Trick
        deps=deps,
    )
    return fach.output
```

`all_messages()` enthält System-Prompt, User-Inputs, Tool-Calls, Tool-Results
und Antworten. Der nächste Agent sieht den ganzen Verlauf.

---

## 6. Checkpointing & Replay in PydanticAI

LangGraph hat dafür `SqliteSaver` + `get_state_history()` + `update_state()`.
PydanticAI hat die **Primitive**, du baust den Workflow.

### Stufe 1: Tool-Retry mit Self-Healing (eingebaut)

```python
from pydantic_ai import ModelRetry

agent = Agent[Deps, str](model="...", retries=2)

@agent.tool
def read_page(ctx, slug: str) -> str:
    if "/" not in slug:
        raise ModelRetry(
            f"Slug '{slug}' braucht ein Verzeichnis-Prefix. "
            f"Versuch z.B. 'massnahmen/{slug}'."
        )
    ...
```

Bei `ModelRetry` schickt PydanticAI den Fehler ans Modell zurück. Es korrigiert
sich. Kein Run-Abbruch.

### Stufe 2: Konversation persistieren

```python
# Run 1
result = await agent.run("Frage", deps=deps)
save_to_db(session_id, result.all_messages())

# Später, frischer Prozess
history = load_from_db(session_id)
result = await agent.run("Mach weiter", message_history=history, deps=deps)
```

Drei Zeilen. Mehr braucht es nicht, um eine Konversation über einen Crash
oder Server-Restart zu retten.

### Stufe 3: Branching / Replay

`all_messages()` ist eine **Liste**. Listen kann man slicen. Damit baut man
sich Time-Travel mit ein paar Zeilen Eigenleistung.

**Konkretes Beispiel:** Der User fragt nach einer Maßnahme, kriegt eine
Antwort — und will dann *aus demselben Zwischenstand* eine alternative
Frage testen, ohne von vorn anzufangen.

```python
import json
from pathlib import Path
from pydantic_ai.messages import ModelMessagesTypeAdapter

CHECKPOINT_DIR = Path("/tmp/agent_checkpoints")
CHECKPOINT_DIR.mkdir(exist_ok=True)


def save_checkpoint(session_id: str, messages: list) -> None:
    """Nach jedem Run die volle Message-Historie wegspeichern."""
    blob = ModelMessagesTypeAdapter.dump_json(messages)
    (CHECKPOINT_DIR / f"{session_id}.json").write_bytes(blob)


def load_checkpoint(session_id: str) -> list:
    blob = (CHECKPOINT_DIR / f"{session_id}.json").read_bytes()
    return ModelMessagesTypeAdapter.validate_json(blob)


async def main():
    deps = Deps(wiki_root=Path("/app/wiki"))

    # --- Run 1: ursprüngliche Frage ---
    result1 = await agent.run(
        "Was ist B1.2 und welche Auflagen gibt es?",
        deps=deps,
    )
    print("Antwort 1:", result1.output)
    save_checkpoint("session_42", result1.all_messages())

    # --- Branch A: Folgefrage in derselben Konversation ---
    history = load_checkpoint("session_42")
    result_a = await agent.run(
        "Und wieviel bekomme ich auf 8 ha?",
        message_history=history,    # ← Verlauf weiterführen
        deps=deps,
    )
    print("Branch A:", result_a.output)

    # --- Branch B: alternative Folgefrage, aus DEMSELBEN Zwischenstand ---
    # Wir laden die Historie nochmal frisch — also AB CHECKPOINT 42, nicht
    # ab dem Ende von Branch A. Damit testen wir einen alternativen Pfad.
    history = load_checkpoint("session_42")
    result_b = await agent.run(
        "Lässt sich B1.2 mit B7 kombinieren?",
        message_history=history,
        deps=deps,
    )
    print("Branch B:", result_b.output)
```

Was hier passiert:

```
                     ┌─→ "Wieviel auf 8 ha?"        → Branch A (Rechen-Antwort)
                     │
[Run 1: "Was ist B1.2?"] ──checkpoint──┤
                     │
                     └─→ "Kombination mit B7?"      → Branch B (Vergleich)
```

Beide Branches sehen denselben Konversationskontext bis zum Checkpoint —
inklusive aller Tool-Calls und gelesenen Wiki-Seiten — und divergieren erst
mit der neuen User-Message. Das Modell muss B1.2 nicht nochmal nachschlagen,
weil das Tool-Result für `read_page("B1.2_...")` schon in der Historie steht.

Drei Anwendungen, für die das nützlich ist:

- **A/B-Tests** über alternative Folge-Prompts ("welche Formulierung gibt die
  bessere Antwort?")
- **What-if-Beratung** in Praxis-Tools: "und was wäre, wenn ich stattdessen
  D2 wählen würde?" — ohne den Kontext zu verlieren.
- **Korrektur-UI**: User klickt "Antwort nicht hilfreich", System bietet zwei
  Re-Runs ab letztem Checkpoint mit unterschiedlichen Prompts.

**Wichtige Subtilität:** Die Historie ist immutable — du musst aufpassen, nicht
versehentlich `result_a.all_messages()` in der DB als neuen Stand zu speichern,
wenn Branch A nur ein Test war. Bei LangGraph nimmt dir das der Checkpointer
ab (jeder Branch hat seine eigene `thread_id`). Bei PydanticAI ist
**Snapshot-Verwaltung deine Verantwortung** — typischerweise eine kleine
Tabelle mit `(checkpoint_id, parent_id, messages_blob)`.

### Was du wirklich vermisst (vs. LangGraph)

| Fähigkeit | Aufwand in PydanticAI |
|---|---|
| Tool-Retry | 0 — eingebaut |
| Konversations-Snapshot | 3 Zeilen + DB-Tabelle |
| Replay an Checkpoint | 5–10 Zeilen Slicing-Logik |
| Branch-Vergleich (mehrere Pfade) | ~20 Zeilen + Checkpoint-Tabelle mit `parent_id` |
| Human-in-the-Loop pause/resume | 20–30 Zeilen Orchestrierung (FastAPI + Storage) |
| Parallele Branches mit Merge | `asyncio.gather` + manueller Merge |
| Graph-Visualisierung | Keine — gibt's nicht |

Das ist alles machbar. Aber:

- Eigenes Checkpointing → **deine** Bugs, nicht die der Library.
- Bei viel Multi-Agent-Komplexität wird der eigene Glue-Code irgendwann
  größer als der Aufpreis für LangGraph.

---

## 7. Entscheidungsmatrix

| Use-Case | Empfehlung |
|---|---|
| Single-Agent, Tool-Belt, Streaming | **PydanticAI** |
| Output muss validiertes Pydantic-Modell sein | **PydanticAI** (Output-Validierung ist Kernfeature) |
| Provider-Wechsel oft / A/B-Tests | **PydanticAI** (Modell ist ein String) |
| Multi-Agent mit klarer Pipeline | PydanticAI (Muster A/B oben) |
| Multi-Agent mit dynamischem Routing über LLM | Beides möglich, knapp PydanticAI |
| Long-running Workflows mit Resumption | **LangGraph** |
| Human-in-the-Loop mit Pause/Resume | **LangGraph** (`interrupt()` eingebaut) |
| Parallele Branches mit komplexem State-Merge | **LangGraph** (Reducer dafür gebaut) |
| Workflow-Visualisierung für Stakeholder | **LangGraph** |
| Regulierte Domäne (Audit, Reproduzierbarkeit) | Tendenz PydanticAI: weniger Magie, leichter zu auditieren |

**Faustregel:** Wenn du den Kontrollfluss auf eine Serviette zeichnen kannst
und nur eine Schleife brauchst — PydanticAI. Wenn du ein Whiteboard mit
Branches und Checkpoints brauchst — LangGraph.

---

## 8. LangChain Academy → PydanticAI Mapping

Falls du den Kurs angehst, was womit lernbar ist:

| LangChain-Academy-Notebook | In PydanticAI ausdrückbar? | Verloren beim Übertragen |
|---|---|---|
| module-0/basics | n/a — reines Provider-Setup | — |
| module-1/simple-graph | Nein — kein User-facing Graph | **Genau das Graph-Konzept** |
| module-1/chain | implizit als `Agent(...)` | Messages-fließen-durch-Knoten-Modell |
| module-1/router | implizit im Tool-Loop | Conditional Edge als Konstrukt |
| module-1/agent | `Agent` + `@agent.tool` | Tool-Loop ist Framework-intern |
| module-1/agent-memory | `message_history=...` | Wie Checkpointer State persistiert |
| module-2/state-* | Gar nicht — LangGraph-spezifisch | Das State-Reducer-Muster |

**Empfehlung:** Wenn du PydanticAI verinnerlicht hast, mach gezielt
`module-1/simple-graph.ipynb` + `module-1/agent.ipynb`. Das sind die
Notebooks, an denen man am meisten *über das Konzept Tool-Loop* lernt —
gerade weil LangGraph zwingt, ihn explizit zu schreiben. Den Rest braucht
man erst bei tatsächlichem LangGraph-Einsatz.

---

## 9. Take-aways

1. **Frameworks sind Trade-offs zwischen Scaffolding und Flexibilität.**
   LangGraph macht Kontrollfluss zu Daten — teurer in Boilerplate, billiger
   in Flexibilität. PydanticAI macht Kontrollfluss zu Framework-Magie —
   billiger in Boilerplate, teurer wenn man Nicht-Standardfälle braucht.

2. **PydanticAI gibt dir die Primitive, LangGraph den Workflow-Layer.**
   Snapshots? `all_messages()`. Resume? `message_history=`. Branching?
   List-Slicing. LangGraph schreibt dir vor *wie* — PydanticAI sagt "hier
   ist die Liste, mach was du willst."

3. **Agenten sind Funktionen.** Das ist der wichtigste PydanticAI-Idiomatik:
   Spezialisten-Agenten als Tools eines Supervisors, oder einfach in
   async-Python orchestriert. Kein Graph, keine State-Schemas, kein Reducer.

4. **Für regulierte Domänen wiegt Auditierbarkeit schwer.** PydanticAI ist
   näher an "lesbares Python", was bei Compliance-Reviews ein Vorteil ist.
   LangGraph-Code mit Reducern und State-Schemas ist ausdrucksstärker, aber
   schwerer durch ein TÜV-Audit zu kriegen.

5. **Lern beides — aber nicht gleichzeitig.** Wenn du PydanticAI verinnerlicht
   hast, reicht ein gezielter LangGraph-Crashkurs (2–3 Stunden), um in
   Architektur-Diskussionen mitreden zu können. Erst die ehrliche Trade-off-
   Diskussion führen können, wenn du beides gebaut hast.
