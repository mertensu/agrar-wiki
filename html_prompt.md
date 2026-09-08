bei html wird die Direktive vor die User-Frage geschoben -> was bedeutet das konkret?

Konkret heißt das: statt nur die Frage an den Agent zu schicken, wird im HTML-Modus ein zweiter Textblock davor gehängt. Aus Sicht des LLM ist der user-Turn dann zweigeteilt – erst Format-Anweisung, dann die Frage:

FORMAT: Antworte als HTML-Fragment (kein <html>, <head>, <body> oder
<script> – nur den Inhalt). Erlaubte Tags: <h2>, <h3>, <p>, <ul>, ...
Für Kombinations-Symbole verwende ausschließlich diese CSS-Klassen:
  - <span class="badge-x">x</span>        – voll kombinierbar
  - <span class="badge-xa">x/a – …</span> – mit Abzug
  ...

FRAGE:
Kann ich B1.2 mit D2 kombinieren?

Im Code (main.py):

prompt = question
if format == "html":
    prompt = f"{HTML_FORMAT_DIRECTIVE}\n\nFRAGE:\n{question}"

async with agent.run_stream(prompt, deps=deps) as result:
    ...

Warum davor und nicht in den System-Prompt: der System-Prompt wird einmal beim Start gebaut und ist für alle Requests bytegleich – das ist Voraussetzung für Geminis implizites Prefix-Caching (siehe prompts.py und agent.py). Würde ich pro Request je nach Modus einen anderen System-Prompt nehmen, wäre der Cache für Markdown-Runs zerstört, sobald ein HTML-Run dazwischen kommt. Im User-Turn hingegen ist die Direktive lokal: Markdown-Anfragen treffen weiter dieselbe gecachte Prefix-Region.

Warum vor der Frage und nicht dahinter: Format-Anweisungen wirken zuverlässiger, wenn das Modell sie liest, bevor es die inhaltliche Frage interpretiert – sonst startet es manchmal mit Markdown und „korrigiert" erst am Ende.

✻ Baked for 17s

❯ aber google gemini modelle nutzen den prefix cache erst ab 30k tokens oder so. die genaue zahl weiss ich nicht

Stimmt, da hast du recht — und mein Cache-Argument ist damit schwächer als ich es verkauft habe.

Gemini 2.5 Pro: implizites Caching greift ab 2.048 Tokens Mindest-Prefix (Flash ab 1.024). Ältere Schwelle war tatsächlich ~32k. Unser System-Prompt mit Verzeichnis-Übersicht + wiki/index.md liegt vermutlich bei ~3-5k Tokens — also knapp über der Schwelle, aber nicht mit großem Polster. Müsste man messen.

Konsequenz für die Implementierung: Der Unterschied „User-Turn vs. System-Prompt" ist hier praktisch egal:
- Liegen wir unter der Schwelle → kein Cache, also nichts zu schützen.
- Liegen wir drüber → die paar hundert Tokens HTML-Direktive würden den Cache nicht killen, sondern nur den Hit auf den gemeinsamen Prefix beschränken (Cache matcht den längsten gemeinsamen Anfang). Bei der Direktive im System-Prompt mit if-Branch hätte ich zwei verschiedene Prefixe – das wäre der echte Cache-Killer. Aber das war eh nicht mein Vorschlag.

Die ehrlicheren Gründe, es im User-Turn zu lassen:
1. Keine Agent-Neukonstruktion pro Request – der Agent wird in lifespan einmal gebaut.
2. Per-Request-Toggle ist semantisch genau das, was hier passiert – Format ist eine Eigenschaft der Anfrage, nicht der Agenten-Identität.
3. Weniger Code – ein f-string statt einer zweiten build_agent-Variante oder PydanticAIs instructions=-Parameter mit Closure.

Wenn du es sauberer willst, wäre der idiomatische Ort PydanticAIs agent.run_stream(question, deps=deps, instructions=HTML_FORMAT_DIRECTIVE) — instructions ist genau für „pro-Run variabel" gedacht (im Gegensatz zu system_prompt). Soll ich darauf umstellen?
