# Codex Master Prompt — Perfect + Token Efficient

Use this prompt when starting implementation in Codex.

```text
Du arbeitest im Repository `kitz-labs/kitz-local-ai-bootstrap`.

ZIEL
Baue KITZLABS AI / LocalAI Command Center Pro vollständig nach der freigegebenen Architektur und den vorhandenen Implementierungsplänen. Qualität, Sicherheit und Tests dürfen niemals zugunsten von Tokenersparnis reduziert werden.

VERBINDLICHE QUELLEN
1. `AGENTS.md`
2. `docs/architecture/master-design.md`
3. relevante Q-Entscheidung aus `docs/architecture/questions-*.md`
4. `docs/superpowers/plans/2026-08-31-kitzlabs-ai-master-implementation-plan.md`
5. aktueller Teilplan

WICHTIG: Lies NICHT bei jedem Task alle Q001-Q326. Suche nur die relevante Entscheidung, wenn Master-Design oder aktueller Plan nicht ausreichen.

ARBEITSMODUS
Nutze Superpowers Subagent-Driven Development, sofern Subagents verfügbar sind.

- niemals direkt auf `main` implementieren
- isolierten Branch/Worktree verwenden
- Master-Plan einmal lesen
- nur den aktuellen Teilplan laden
- pro Task nur Task-Brief + relevante Dateien/Interfaces laden
- zuerst gezielt suchen, nicht das ganze Repo lesen
- große Dateien nur in relevanten Bereichen öffnen
- Fortschritt dauerhaft im Superpowers-Ledger speichern
- abgeschlossene Tasks niemals erneut ausführen
- gleiche kleine mechanische Änderungen sinnvoll bündeln
- keine doppelte Reviewer-Arbeit
- keine komplette Historie in neue Subagent-Prompts kopieren
- Artefakte, Diffs, Reports und Briefs über Dateipfade übergeben

MODELLWAHL
Verwende immer das günstigste Modell, das die Aufgabe zuverlässig in einem Durchgang lösen kann:
- mechanisch/eindeutig: fast/cheap
- Integration/Debugging: standard
- Security/Architektur/finales Review: stärkstes verfügbares Modell
- Fix-Runde 4–5: mindestens eine Stufe stärker als gescheiterter Implementer

Wenn lokale KITZ/LocalAI-Worker verfügbar sind, dürfen risikoarme mechanische Analyse-, Zusammenfassungs- und Refactoring-Aufgaben lokal laufen. Kritische Integration, Security und finales Review bleiben bei Codex/starkem Reviewer.

TESTS
Teststrategie von klein nach groß:
1. gezielter Test der Änderung
2. betroffener Modul-/Package-Test
3. Integrationstest nur wenn Grenze betroffen
4. Phase-Suite nach Subsystem
5. vollständige Acceptance-Suite am Ende

Keine Full-Suite nach jeder Kleinigkeit. Aber keine Änderung ohne passende Tests.

SICHERHEIT
Nie umgehen:
- Smart Guard
- Secret Vault / Keychain
- Capability Policies
- Audit Logging
- Snapshots/Recovery bei riskanten Änderungen
- LocalAI REST/MCP/Skill-Prompt-Synchronisierung

Keine Secrets, Tokens, `.env`-Inhalte, persönlichen Memory-Rohdaten oder Modell-Binaries committen oder ausgeben.

LOCALAI
Bei LocalAI-Core/Admin-Änderungen gegebenenfalls synchron halten:
1. REST Endpoint
2. MCP Tool/Client
3. Skill Prompt
4. Tests

Vor Aktivierung: Build/Test/Benchmark. Bei Regression: Rollback.

TOKEN-SPARREGELN
- keine wiederholten Komplettlesungen unveränderter Docs
- keine wiederholten Architektur-Zusammenfassungen
- keine unnötigen Repo-Weitscans
- keine kompletten Logs, wenn relevante Fehlerzeilen reichen
- keine ganzen Diffs in Prompts, wenn Review-Package-Datei existiert
- keine erneute Modellrecherche, wenn Qualification-Ergebnis schon gespeichert ist
- keine leistungsstarken Modelle für reine Transkription/mechanische Tasks

AUSGABE WÄHREND DER ARBEIT
Halte Routine-Updates extrem kurz:
Task N: DONE
Changed: <Pfade>
Tests: <Befehl> — PASS
Commit: <SHA>
Concerns: none|<kurz>

Nur bei Fehler, Security-Ruling, Plan-Konflikt oder Abschluss ausführlicher berichten.

START
1. Lies `AGENTS.md`.
2. Lies den Master-Implementierungsplan.
3. Prüfe Ledger/Git-Historie auf bereits erledigte Tasks.
4. Beginne beim ersten noch nicht erledigten Task des ersten unvollständigen Teilplans.
5. Arbeite kontinuierlich Task für Task bis zu einem echten Stop-Grund oder bis alles abgeschlossen und final reviewed ist.
```

## Kurzstart

Wenn Codex das Repository bereits geöffnet hat, reicht künftig:

```text
Arbeite nach `AGENTS.md` und `docs/codex/MASTER_PROMPT.md` weiter. Resume anhand Ledger + Git-Historie beim ersten unvollständigen Task. Token-effizient arbeiten, aber alle Qualitäts-, Test-, Security- und Review-Gates vollständig einhalten.
```
