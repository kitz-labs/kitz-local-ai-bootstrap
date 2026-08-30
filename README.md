# KITZLABS AI — LocalAI Command Center Pro

> Lokales, deutschsprachiges KI-Betriebssystem für Apple Silicon mit LocalAI als Core und einem eigenen KITZLABS Control Layer als zentrale Steuerung.

## Status

**Phase:** Architektur abgeschlossen / Implementierung noch nicht gestartet

- Architekturentscheidungen: **Q001–Q326**
- Standardentscheidung: **Empfehlung E**, sofern keine Fragennummer ausdrücklich überschrieben wird
- Plattform: **macOS / Apple Silicon / 16 GB Unified Memory**
- Inference-Core: **LocalAI**
- Oberfläche: **KITZLABS AI Command Center Pro**
- Betriebsmodell: **Local-first, hochautonom, Smart Guard für kritische Aktionen**

## Ziel

KITZLABS AI soll eine einzige lokale Oberfläche für folgende Bereiche bereitstellen:

- Chat und Coding
- autonome Agenten und Agenten-Teams
- Projekte, Aufgaben und Workflows
- Memory, Wissen, RAG und Knowledge Graph
- Skills und Prompt Intelligence
- MCP, APIs und Connector Center
- GitHub Intelligence
- Browser, Research und Scraping
- Python App Operator
- Telegram Gateway
- Modellverwaltung, Routing und Benchmarks
- Hugging Face Modell-Installer
- LocalAI Core Engineer
- Bild- und Videostudio
- System Health, Recovery und Zeitmaschine
- Security, Secret Vault und Smart Guard

## Kernarchitektur

```text
KITZLABS AI Command Center Pro
            |
            v
KITZLABS Control Layer
            |
            +--> Smart Orchestrator
            +--> Context / Memory / Knowledge
            +--> Model Router / Resource Governor
            +--> Tasks / Workflows / Scheduler
            |
            v
KITZ Tool Gateway
            |
            +--> Smart Guard
            +--> Capability Policy
            +--> Audit / Recovery
            |
            +--> LocalAI Core
            +--> GitHub
            +--> Browser / Research / Scraping
            +--> MCP / APIs / Connector Center
            +--> Telegram
            +--> Python Apps
```

## Modellrollen

Die Oberfläche arbeitet mit stabilen Rollen statt mit fest verdrahteten Modellnamen:

| Rolle | Zweck |
|---|---|
| `kitz-main` | allgemeiner Hauptagent / Chat / Planung |
| `kitz-code` | Coding, Debugging, LocalAI-Entwicklung |
| `kitz-fast` | schnelle leichte Aufgaben |
| `kitz-embed` | Embeddings / RAG / semantische Suche |

Der Model Router darf Modelle nach Benchmark, Aufgabe, RAM-Verbrauch und Qualität automatisch zuordnen.

## Hauptagenten

- **KITZ Master** — zentrale Koordination und Delegation
- **Coding Pro** — Code, Tests, Refactoring und Debugging
- **Research** — Web-Recherche, Quellen und Wissensaufbau
- **Mac Operator** — lokale macOS-Aufgaben innerhalb freigegebener Bereiche
- **DevOps** — Services, Prozesse, Deployment und Diagnose
- **KITZ LocalAI Entwickler** — LocalAI Core, Modelle, Backends, MCP, Agenten, UI, CLI, Konfiguration und Tests
- **KITZ Python App Operator** — lokale Python-Anwendungen erkennen, starten, stoppen, reparieren und verwalten

## Autonomie

KITZLABS AI arbeitet standardmäßig hochautonom innerhalb freigegebener Projekt- und Systemgrenzen.

Automatisch erlaubt sind unter anderem:

- Dateien innerhalb freigegebener Projekte lesen und ändern
- Code erstellen und reparieren
- Tests und Benchmarks starten
- Git-Branches und Commits erzeugen
- Agenten und Unteraufgaben starten
- Browser- und Research-Aufgaben ausführen
- Projektwissen und Memory pflegen
- Skills und Prompts testen und verbessern
- Python Apps starten, stoppen und reparieren
- LocalAI-Konfigurationen und Modelle verwalten
- Snapshots und Rollbacks erzeugen

Kritische oder irreversible Aktionen bleiben unter **Smart Guard**.

## Vollbild-Oberfläche

Die App nutzt die komplette Browser- bzw. Desktopfläche.

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ PROJEKT ● HEALTH │ AUTOPILOT ● │ CHAT │ AUFGABE │ AGENT │ DIAGNOSE        │
├──────────────┬──────────────────────────────────────────────────┬────────────┤
│ NAVIGATION   │ HEALTH / TASKS / AGENTEN / FEHLER / MODELLE     │ LIVE       │
│              ├────────────────────────┬─────────────────────────┤            │
│ Übersicht    │ AKTIVE ARBEIT         │ WARNUNGEN               │ RAM        │
│ Aufgaben     ├────────────┬───────────┴─────────────────────────┤ CPU        │
│ Chats        │ AUFGABEN   │ DATEIEN / GITHUB                  │ LocalAI    │
│ Dateien      ├────────────┴─────────────────────────────────────┤ GitHub     │
│ Wissen       │ HUGGING FACE / MODELLE                         │ HF         │
│ Agenten      ├────────────────────────┬─────────────────────────┤ Metal      │
│ GitHub       │ AKTIVITÄTEN           │ ZEITMASCHINE            │ Autopilot  │
└──────────────┴────────────────────────┴─────────────────────────┴────────────┘
```

Eigenschaften:

- linke Smart Sidebar einklappbar
- rechte Live-Leiste offen, kompakt oder versteckt
- Sticky Projektkopf
- Karten per Drag & Drop verschiebbar
- Karten frei skalierbar
- Layout pro Projekt speicherbar
- keine großen ungenutzten Außenränder

## Architektur-Dokumentation

Die vollständigen Entscheidungen liegen unter `docs/architecture/`.

| Datei | Inhalt |
|---|---|
| `docs/architecture/master-design.md` | Gesamtarchitektur |
| `docs/architecture/questions-001-085.md` | Kernentscheidungen und Cockpit |
| `docs/architecture/questions-086-166.md` | Agenten, Modelle, Memory, Skills, LocalAI |
| `docs/architecture/questions-167-246.md` | MCP, APIs, Browser, GitHub, Telegram, Security, Recovery |
| `docs/architecture/questions-247-326.md` | Medien, Installation, Datenhaltung, Updates, UI, Tests und Abschluss |
| `docs/architecture/README.md` | Index und Änderungsregeln |

## Entscheidungsregel

Jede wichtige Architekturentscheidung hat eine feste ID.

Beispiel:

```text
Q107=C
```

Bedeutung: Nur Entscheidung `Q107` wird auf Variante `C` geändert. Danach müssen die betroffenen Spec-, Plan-, Test- und Dokumentationsstellen synchronisiert werden.

Ohne explizite Änderung gilt weiterhin die dokumentierte Empfehlung.

## Geplante Repository-Struktur

```text
kitz-local-ai-bootstrap/
├── README.md
├── docs/
│   ├── architecture/
│   └── superpowers/
├── cockpit/
├── control-layer/
├── agents/
├── skills/
├── prompts/
├── routing/
├── policies/
├── benchmarks/
├── tests/
├── migrations/
├── installer/
└── scripts/
```

Keine Secrets, persönlichen Memory-Rohdaten oder Modell-Binaries gehören in GitHub.

## Nächster Build-Ablauf

Die Implementierung wird nicht als ein riesiger Schritt ausgeführt. Sie wird in testbare Subsysteme zerlegt.

Empfohlene Reihenfolge:

1. **Foundation** — Repository-Struktur, Konfiguration, Datenpfade, Logging
2. **Control Layer** — zentrale APIs, State und Event-System
3. **LocalAI Integration** — Core, Modellrollen und Health Checks
4. **Tool Gateway + Smart Guard** — Rechte, Policies, Audit
5. **Projekt- und Task-System** — Projekte, Aufgaben, Scheduler
6. **Agent Orchestrator** — KITZ Master und Spezialagenten
7. **Memory / Knowledge / RAG** — SQLite + lokaler Vector Index
8. **Model Router / Resource Governor** — Apple-Silicon-/RAM-Steuerung
9. **GitHub / Browser / MCP / APIs / Telegram** — externe Connectoren
10. **Python App Operator** — lokale Anwendungen
11. **Cockpit UI** — Vollbild-Dashboard und alle Seiten
12. **Recovery / Security / Backup** — Zeitmaschine, Vault, Restore
13. **Acceptance Tests** — Core, Agenten, Tools, Security und Performance
14. **One-Command Installer** — saubere Neuinstallation und Migration

## Qualitätsregel

Jedes Subsystem muss vor Aktivierung:

1. isoliert testbar sein,
2. Fehler sauber melden,
3. auditierbare Aktionen erzeugen,
4. einen definierten Recovery-Pfad besitzen,
5. auf dem Ziel-Mac mit 16 GB Unified Memory geprüft werden.

## GitHub Workflow

Änderungen sollen über Branch → Tests → Pull Request → Review → Merge laufen.

Autonome Agenten dürfen Branches, Commits, Issues und Pull Requests vorbereiten. Kritische Merges und produktive Änderungen bleiben durch die Capability Policy geschützt.

---

**KITZLABS AI** — Local-first. Projektbezogen. Agentisch. Kontrolliert autonom.
