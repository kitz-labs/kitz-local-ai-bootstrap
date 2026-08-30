# KITZLABS AI / LocalAI – Master Design

Stand: 2026-08-30

## 1. Ziel

Ein lokales, deutschsprachiges KI-Betriebssystem für Apple Silicon mit 16 GB Unified Memory. Das tägliche Produkt ist das **KITZLABS AI Command Center Pro**. LocalAI ist der lokale Inference-/Agent-Core dahinter, nicht die primäre Benutzeroberfläche.

## 2. Kernarchitektur

```text
KITZLABS Cockpit
      |
      v
KITZLABS Control Layer
      |
      +--> Smart Orchestrator
      +--> Context / Memory / Knowledge
      +--> Model Router / Resource Governor
      +--> Task / Workflow / Scheduler
      |
      v
KITZ Tool Gateway
      |
      +--> Smart Guard / Capability Policy / Audit
      |
      +--> LocalAI Core
      +--> GitHub
      +--> Browser / Research / Scraping
      +--> MCP / APIs / Connector Center
      +--> Telegram
      +--> Python App Operator
      +--> lokale Dateien / Git / Terminal
```

## 3. Modellrollen

Stabile Aliase statt harter Modellnamen:

- `kitz-main` – allgemeiner Chat, Planung, Orchestrierung
- `kitz-code` – Coding, LocalAI Core Engineer, komplexe technische Aufgaben
- `kitz-fast` – schnelle leichte Aufgaben
- `kitz-embed` – Embeddings / Retrieval

Der Model Router darf konkrete Modelle nach Benchmark, RAM, Metal, Geschwindigkeit, Kontext und Aufgabe austauschen. Große Modelle werden dynamisch geladen/entladen.

## 4. Agenten

Start-Agenten:

- KITZ Master
- Coding Pro
- Research
- Mac Operator
- DevOps
- KITZ LocalAI Entwickler
- KITZ Python App Operator

KITZ Master ist der Standard-Orchestrator. Komplexe Aufgaben werden in Teilaufgaben zerlegt und bei Bedarf parallel an Spezialagenten verteilt. Jeder Agent arbeitet nur innerhalb seiner Capability Policy.

## 5. LocalAI Core Engineer

Der LocalAI-Entwickler darf innerhalb des LocalAI-Domains Modelle, YAMLs, Aliase, Backends, APIs, MCP-Tools, Skills, Agenten, Prompts, Go-Code, Web-UI, CLI, Metal-Backend, Galleries, Services und Routing ändern.

Pflichtablauf für mutierende Änderungen:

1. Snapshot / Backup
2. Branch oder isolierter Worktree
3. Änderung
4. Build
5. Unit Tests
6. Integration / Smoke Tests
7. Modell-/Agententest falls relevant
8. Performance-/RAM-Vergleich falls relevant
9. Aktivierung nur bei erfolgreichem Ergebnis
10. sonst Rollback / Quarantäne

Bei Änderungen an LocalAI Admin-Funktionen müssen REST-Endpunkt, MCP-Tool/Client und zugehöriger Skill-/Prompt-Layer synchron gehalten und getestet werden.

## 6. Autonomie

Standard: **maximale Autonomie innerhalb explizit freigegebener Projektgrenzen**.

Automatisch erlaubt, wenn Policy es zulässt:

- Projektdateien lesen/erstellen/ändern/verschieben/löschen
- Code ändern
- Tests/Benchmarks ausführen
- isolierte Abhängigkeiten installieren
- Git Branches/Commits/PRs vorbereiten
- Python Apps starten/stoppen/reparieren
- Browser/Research/APIs/MCP verwenden
- LocalAI-Konfigurationen ändern
- Skills/Prompts/Memory/Knowledge verbessern
- Snapshots/Rollbacks durchführen

Geschützt bleiben:

- Secrets offenlegen
- Safety Core deaktivieren
- kritische irreversible Systemänderungen außerhalb Scope
- größere Datenlöschungen ohne sicheren Restore
- nicht freigegebene externe/produktive Aktionen

## 7. Memory / Knowledge

Getrennte Ebenen:

- persönliches Memory
- Projekt-Memory
- Fehler-/Lösungs-Memory
- Erfolgs-/Workflow-Muster
- temporärer Task-Kontext
- Knowledge Base
- Knowledge Graph

Metadaten: SQLite. Retrieval: separater lokaler Vektorindex. Quelle bleibt rekonstruierbar; Vektorindex muss rebuildbar sein. Secrets gelangen weder in Memory noch Knowledge.

## 8. Prompt / Skill Intelligence

Prompt-Hierarchie:

```text
Global Base
  + Agent Prompt
  + Project Prompt
  + Skill Prompt
  + Task Context
```

Prompts und Skills sind versioniert, benchmarkbar und rücksetzbar. Wiederholte erfolgreiche Muster können Skill-Kandidaten erzeugen. Neue oder externe Skills werden vor Aktivierung auf Quelle, Rechte, Sicherheit, Sandbox-Verhalten und Nutzen geprüft.

## 9. GitHub

GitHub ist Source of Truth für nicht-sensible Systemdefinitionen:

- agents/
- skills/
- prompts/
- routing/
- policies/
- benchmarks/
- tests/
- docs/
- migrations/
- installer/
- cockpit/
- control-layer/

Nicht in GitHub:

- Secrets
- persönliche Memory-Rohdaten
- private Chat-Rohdaten
- Modell-Binaries
- private Backups

Normaler Flow: Branch -> Änderung -> Tests -> Commit -> PR. Kritische Merge-/Production-Aktionen bleiben Smart-Guard-gebunden.

## 10. Projekt-Hub / UI

Die App nutzt die **gesamte Browserfläche**.

```text
+----------------------------------------------------------------------------------+
| PROJEKT | Health | Autopilot | Chat | Aufgabe | Agent | Diagnose | GitHub | HF  |
+----------+-----------------------------------------------------------+-----------+
| NAV      | KPI: Health | Tasks | Agenten | Fehler | GitHub | Modelle | LIVE      |
|          +-----------------------------+-----------------------------+           |
| Übersicht| Aktive Arbeit               | Warnungen / nächste Schritte| RAM/CPU   |
| Aufgaben +-------------------+---------+-----------------------------+ LocalAI   |
| Chats    | Aufgaben          | Dateien / GitHub                     | GitHub    |
| Dateien  +-------------------+--------------------------------------+ HF        |
| Wissen   | Modelle / Hugging Face     | Projektwissen               | Metal     |
| Memory   +-----------------------------+-----------------------------+ Agenten    |
| ...      | Aktivitäten                | Zeitmaschine                | Autopilot |
+----------+-----------------------------+-----------------------------+-----------+
```

Eigenschaften:

- linke Smart Sidebar: breit / Icons / automatisch kompakt
- rechte Live-Bar: offen / kompakt / versteckt
- Sticky Projektkopf
- responsive Vollbildnutzung ohne Max-Width-Leerraum
- Karten Drag & Drop, Resize, Hide
- Layout pro Projekt speichern
- kurze deutsche UI-Texte; technische Details aufklappbar

## 11. Seiten / Module

Globale Hauptbereiche:

1. Übersicht
2. Neuer Chat
3. Chats
4. Aufgaben
5. Aktivitäten
6. Projekte
7. Dateien
8. Wissen
9. Gedächtnis
10. Wissensgraph
11. Kontext
12. Agenten-Zentrale
13. LocalAI-Entwickler
14. Python-Anwendungen
15. Arbeitsabläufe
16. Zeitpläne
17. Prompt-Bibliothek
18. Skills
19. Terminal
20. Browser
21. Web-Recherche
22. API-Zentrale
23. MCP
24. Verbindungen
25. GitHub
26. Telegram
27. Modelle
28. Modell-Routing
29. Bildstudio
30. Videostudio
31. LocalAI
32. Systemkarte
33. Systemzustand
34. Fehleranalyse
35. Zeitmaschine
36. Sicherungen
37. Sicherheit
38. Erweiterungen
39. Einstellungen

## 12. Python App Operator

Scannt nur freigegebene Ordner. Erkennt Startmethoden und Dependencies. Standardmäßig eigene `uv`-Umgebung pro App. UI-Aktionen: Start, Stop, Restart, Logs, Open, Repair. Verifizierte Startbefehle werden als App-Metadaten gespeichert.

## 13. Browser / Research / File Intelligence

- Playwright für deterministische Browser-Automation
- agentischer Browser für komplexe visuelle Abläufe
- Crawl4AI/vergleichbare strukturierte Extraktion für Web/RAG
- MarkItDown/vergleichbare sichere Konvertierung für Office/PDF, wo passend
- Watchfiles/Event Bus für Dateiänderungen

## 14. Installation / Migration

Ziel: One-Command Bootstrap + Smart Setup Wizard.

Ablauf:

1. Preflight Mac/Apple Silicon/RAM/Storage/Ports/Tools
2. vollständiges Backup Altbestand
3. Inventar LocalAI/Ollama/HF-Caches
4. nur valide Daten/Modelle übernehmen
5. zentralen `~/KITZLABS-AI` Root anlegen
6. native/isolierte Dependencies installieren
7. LocalAI + Control Layer + Cockpit konfigurieren
8. Modelle registrieren/benchmarken
9. Agenten/Tools/Policies initialisieren
10. Health/Acceptance Tests
11. Launcher/Autostart aktivieren
12. Abschlussbericht

Ollama bleibt installiert, wird in V1 aber nicht in das neue System integriert.

## 15. Ordnerstruktur

```text
~/KITZLABS-AI/
  apps/
  models/
  agents/
  skills/
  memory/
  knowledge/
  projects/
  config/
  logs/
  backups/
  cache/
```

## 16. Recovery / Backup

Vor relevanten mutierenden Aktionen entsteht ein Snapshot oder äquivalenter Rückfallpunkt. Ein Stand gilt erst nach erfolgreichen Tests und Health Checks als stabil. Regressionen können automatisch zurückgerollt werden.

## 17. Tests / Release Gate

Pflicht:

- Core Unit/Integration/Smoke
- Agent/Tool/Recovery/Rechte
- Modelle: Qualität, RAM, Speed, Stabilität
- MCP/API: Schema, Auth, Rechte, Fehlerfälle
- Security: Secret-Leak, Scope Escape, gefährliche Aktionen
- UI: Navigation, responsive Vollbildansicht, Kerninteraktionen
- Performance Baselines
- Recovery Test

Release nur bei grünen Pflichtchecks.

## 18. Entscheidungsregister

Die kanonische Änderungsmatrix befindet sich in:

- `questions-001-085.md`
- `questions-086-166.md`
- `questions-167-246.md`
- `questions-247-326.md`

Eine spätere Änderung wird über die Q-ID referenziert, z. B. `Q107=C`. Diese ID bleibt dauerhaft stabil.
