# Fragen Q247–Q326 – Medien, Installation, Daten, Updates, UI, Monitoring, Tests, Abschluss

Für alle Fragen gilt aktuell: **Empfehlung E = Entscheidung E**.

## Antwortschema

- **A** minimal/manuell
- **B** Basis
- **C** erweitert
- **D** hochautomatisiert
- **E** ⭐ vollständig integriert, autonom in freigegebenen Grenzen, getestet und rücksetzbar

## Lokales Bildstudio – Q247–Q252

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 247 | Wie wird lokale Bildgenerierung integriert? | E – eigenes Bildstudio im Cockpit |
| 248 | Wie werden Bildmodelle verwaltet? | E – Modellregistry + Kompatibilitätscheck + Rollen |
| 249 | Wie werden Bildjobs ausgeführt? | E – Queue mit Ressourcensteuerung |
| 250 | Wie werden Prompts/Presets gespeichert? | E – projektbezogene Vorlagen mit Versionierung |
| 251 | Wie werden Ergebnisse Projekten zugeordnet? | E – automatische Ablage, Metadaten und Verlauf |
| 252 | Wie wird bei knappen Ressourcen priorisiert? | E – Resource Governor priorisiert Text/Agenten vor schweren Medienjobs |

## Lokales Videostudio – Q253–Q258

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 253 | Wie wird lokale Videogenerierung integriert? | E – eigenes Videostudio im Cockpit |
| 254 | Wie werden Videomodelle verwaltet? | E – Registry + Mac/RAM-Kompatibilität + Benchmarks |
| 255 | Wie werden lange Videojobs behandelt? | E – Queue, Pause/Resume soweit Backend möglich, Status und Logs |
| 256 | Wie werden Video-Vorlagen gespeichert? | E – projektbezogene Presets und Workflows |
| 257 | Wie werden Medienjobs mit Agenten verbunden? | E – Agent kann Job planen, starten, prüfen und Ergebnis zuordnen |
| 258 | Wie werden fehlgeschlagene Medienjobs behandelt? | E – Diagnose, sichere Wiederholung, alternative Einstellungen/Modelle |

## Installation / Migration / One-Command Setup – Q259–Q270

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 259 | Wie startet die Neuinstallation? | E – One-Command Bootstrap mit Preflight |
| 260 | Was prüft der Preflight? | E – macOS/Apple Silicon, RAM, Speicher, Tools, Ports, alte Installationen |
| 261 | Wie werden bestehende Daten gesichert? | E – vollständiger Snapshot vor Änderungen |
| 262 | Wie werden alte LocalAI-Daten analysiert? | E – Inventar + Klassifikation in übernehmen/archivieren/verwerfen |
| 263 | Wie werden alte Modelle übernommen? | E – Hash/Format/Kompatibilität prüfen und nur valide Modelle migrieren |
| 264 | Wie wird Ollama behandelt? | E – erkennen und unangetastet lassen; keine Integration in V1 |
| 265 | Wie werden Abhängigkeiten installiert? | E – möglichst nativ/isoliert, reproduzierbar und versioniert |
| 266 | Wann wird Docker verwendet? | E – nur wenn eine Komponente davon klar profitiert oder es zwingend braucht |
| 267 | Wie werden Ports und Dienste gewählt? | E – Preflight erkennt Konflikte und vergibt dokumentierte stabile Werte |
| 268 | Wie wird der Installer getestet? | E – Dry Run, idempotente Wiederholung, Smoke Tests und Recovery |
| 269 | Wie wird ein fehlgeschlagenes Setup behandelt? | E – sauberer Rollback auf Ausgangszustand |
| 270 | Wie endet das Setup? | E – Health Check, Benchmarks, Startmodelle, Launcher und Abschlussbericht |

## Ordnerstruktur / Datenhaltung – Q271–Q276

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 271 | Wo liegt der zentrale KITZLABS Root? | E – standardisiert unter `~/KITZLABS-AI` mit konfigurierbarem Root |
| 272 | Welche Hauptordner gibt es? | E – apps, models, agents, skills, memory, knowledge, projects, config, logs, backups, cache |
| 273 | Wo liegen strukturierte Metadaten? | E – SQLite pro klarer Verantwortlichkeit, keine monolithische Alles-DB |
| 274 | Wo liegen Vektordaten? | E – separater lokaler Vektorindex mit rebuildbarer Quelle |
| 275 | Wie werden große Modell-/Cache-Dateien behandelt? | E – außerhalb Git, über Registry/Manifest referenziert |
| 276 | Wie werden Datenportabilität und Restore gesichert? | E – dokumentierte Export-/Import-Formate + Backups |

## Updates / Selbstverbesserung / Versionierung – Q277–Q284

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 277 | Wie werden Systemupdates erkannt? | E – Update Intelligence mit Quellen- und Versionsprüfung |
| 278 | Wie werden Updates ausgerollt? | E – Staging -> Tests -> Canary -> Aktivierung |
| 279 | Dürfen interne Prompts/Skills automatisch aktualisiert werden? | E – ja, wenn Benchmarks besser und Safety unverändert |
| 280 | Dürfen Agenten eigene Routings optimieren? | E – ja, versioniert und messbar |
| 281 | Wie werden Verschlechterungen erkannt? | E – Vergleichsbenchmarks + Health/Erfolgsmetriken |
| 282 | Was passiert bei Regression? | E – automatischer Rollback und Quarantäne der Version |
| 283 | Wie werden Änderungen nachvollziehbar gemacht? | E – Version, Grund, Testresultat, Autor/Agent, Zeitpunkt |
| 284 | Wie wird Selbstverbesserung begrenzt? | E – unveränderlicher Safety Core + Ressourcen-/Scope-Grenzen |

## UI / Design / Responsivität – Q285–Q296

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 285 | Welches Grundlayout gilt? | E – Dark Premium Vollbild-Desktop-Cockpit |
| 286 | Nutzt die App die gesamte verfügbare Fläche? | E – ja, ohne unnötige Max-Width-Ränder |
| 287 | Wie verhält sich die linke Navigation? | E – breit, Icon-Modus, automatisch kompakt |
| 288 | Wie verhält sich die rechte Live-Bar? | E – offen, kompakt oder versteckt |
| 289 | Wie verhalten sich Header und Statusleiste? | E – wichtige Bereiche sticky |
| 290 | Wie werden Dashboard-Karten angeordnet? | E – responsive Grid + Drag/Resize/Hide |
| 291 | Wie werden Layouts gespeichert? | E – pro Projekt + globales Standardlayout |
| 292 | Wie wird auf kleineren Fenstern reagiert? | E – Sidebars komprimieren, Karten stapeln, Kernaktionen erhalten |
| 293 | Wie werden Live-Daten aktualisiert? | E – ereignisbasiert/gezielt, keine unnötigen Voll-Refreshes |
| 294 | Wie werden technische Details dargestellt? | E – kurze Zusammenfassung, Details aufklappbar |
| 295 | Wie wird deutsche Sprache umgesetzt? | E – alle UI-Texte Deutsch, Produkt-/Techniknamen unverändert |
| 296 | Wie wird Bedienung mit Maus und Tastatur optimiert? | E – klare Hover/Focus-Zustände, Shortcuts und zugängliche Navigation |

## Logs / Audit / Aktivitäten / Monitoring – Q297–Q302

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 297 | Welche Aktivitäten werden protokolliert? | E – Agent, Tool, Terminal, Git, Datei, Modell, Policy, Recovery |
| 298 | Wie detailliert sind Standardlogs im UI? | E – kompakte Zusammenfassung, Rohdetails auf Abruf |
| 299 | Wie werden Logs aufbewahrt? | E – Smart Retention + Größenlimits + Rotation |
| 300 | Wie werden sensible Daten in Logs behandelt? | E – automatische Redaction vor Speicherung |
| 301 | Wie werden Aktivitäten durchsucht? | E – Filter + Volltext + semantische Suche |
| 302 | Wie wird Monitoring visualisiert? | E – Live Timeline + Health Center + System Map |

## Performance / Tests / Acceptance – Q303–Q310

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 303 | Welche Core-Tests sind Pflicht? | E – Unit + Integration + Smoke |
| 304 | Welche Agenten-Tests sind Pflicht? | E – Aufgabenqualität, Tool-Nutzung, Recovery, Rechte |
| 305 | Welche Modelltests sind Pflicht? | E – Qualität, Geschwindigkeit, RAM, Stabilität, Kontext |
| 306 | Welche MCP/API-Tests sind Pflicht? | E – Schema, Auth, Rechte, Fehlerfälle, Health |
| 307 | Welche Security-Tests sind Pflicht? | E – Secret-Leak, Scope Escape, gefährliche Aktionen, Audit |
| 308 | Welche UI-Tests sind Pflicht? | E – Kernnavigation, Responsivität, Status, wichtige Interaktionen |
| 309 | Wie wird Performance-Regressionsschutz umgesetzt? | E – gespeicherte Baselines + Schwellenwerte |
| 310 | Wann gilt ein Release als akzeptiert? | E – alle Pflichtchecks grün + Health/Recovery getestet |

## Extension Hub / Skill Scout – Q311–Q316

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 311 | Welche Erweiterungen kann der Hub verwalten? | E – Skills, MCPs, Agenten, Tools, Connectoren |
| 312 | Woher dürfen Erweiterungen kommen? | E – kuratierte Quellen + GitHub/Links mit Trust-Prüfung |
| 313 | Wie werden neue Erweiterungen geprüft? | E – statische Prüfung + Rechteanalyse + Sandbox + Benchmark |
| 314 | Dürfen Erweiterungen automatisch aktiviert werden? | E – nur wenn risikoarm und Tests vollständig grün sind |
| 315 | Wie werden Erweiterungen aktualisiert? | E – staged + diff + rollback |
| 316 | Wie werden ungeeignete Erweiterungen behandelt? | E – blockieren/quarantänisieren mit Begründung |

## Finaler Gesamtcheck – Q317–Q326

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 317 | Ist Local-First die Standardstrategie? | E – ja |
| 318 | Ist das KITZLABS Cockpit die tägliche Hauptoberfläche? | E – ja |
| 319 | Bleibt LocalAI Core hinter dem Control Layer austausch-/wartbar? | E – ja, klare Schnittstellen |
| 320 | Sind alle autonomen Aktionen projekt- und policy-gebunden? | E – ja |
| 321 | Sind Secrets, Memory, Modelle und Git-Daten sauber getrennt? | E – ja |
| 322 | Ist jede relevante Änderung versioniert und rücksetzbar? | E – ja |
| 323 | Kann jede große Funktion unabhängig getestet werden? | E – ja, modulare Grenzen |
| 324 | Ist das System für 16 GB Apple Silicon ressourcenbewusst? | E – ja, dynamisches Scheduling/Load-Unload |
| 325 | Ist jede Entscheidung über Q-Nummer später änderbar? | E – ja, diese Matrix ist Source of Truth |
| 326 | Ist die Architektur bereit für die Umsetzung in getrennten, testbaren Teilplänen? | E – ja, nach Review dieses Branches |

# Abschlussstatus

- Q001–Q326 sind als kanonische Entscheidungs-IDs dokumentiert.
- Offene Standardentscheidung: keine; alle noch nicht individuell geänderten Punkte stehen auf der ⭐ Empfehlung.
- Änderungen erfolgen künftig über die Fragennummer und werden in Spec/Plan/Tests synchron nachgezogen.
