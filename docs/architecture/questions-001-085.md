# Fragen Q001–Q085 – bestätigte Entscheidungen

Diese Fragen wurden im Design-Dialog bereits entschieden. Wo mehrere Optionen gewählt wurden, ist das ausdrücklich angegeben.

| Q | Entscheidungsfrage | Aktuelle Entscheidung |
|---:|---|---|
| 1 | Welche Kernfunktionen gehören in Version 1? | A – Core Pro: Chat, Coding, Agents, Memory, Skills, Knowledge/RAG, MCP |
| 2 | Welche Oberfläche wird täglich genutzt? | E – eigenes KITZLABS Cockpit + separates LocalAI Admin |
| 3 | Welche Modellrollen gibt es? | A+B+C+D – main, code, fast, embed |
| 4 | Welche Start-Agenten werden vorkonfiguriert? | A+B+C+D+E – Master, Coding Pro, Research, Mac Operator, DevOps |
| 5 | Welche MCP-Pakete kommen in V1? | A+B+C+D – Local Developer, GitHub, Notion, Browser/Web |
| 6 | Welche Memory-Arten werden geführt? | A+B+C+D – persönlich, Projekt, Erfolg/Fehler, kontrollierte Verbesserung |
| 7 | Welche lokalen Rechte dürfen Agenten nutzen? | A+B+C+D – lesen/analysieren, Projektdateien ändern, Terminal mit Schutz, Git/Browser |
| 8 | Welche Laufzeitarchitektur auf Apple Silicon? | D – Hybrid nativ/Metal, Docker nur wo nötig |
| 9 | Wie wird Cloud-Nutzung behandelt? | B – local first, Cloud nur explizit manuell |
| 10 | Wie werden riskante Aktionen behandelt? | D – Smart Guard |
| 11 | Wie läuft Wartung? | D – Safe Auto Maintenance |
| 12 | Wie ist das Cockpit aufgebaut? | D + ausgewählte E-Module – festes Premium-Layout + modulare Panels |
| 13 | Welche Hauptbereiche sind dauerhaft sichtbar? | A+B+C+D – Chat/Agents, Projekte/Memory, Skills/MCP, Modelle/Routing |
| 14 | Wie werden Dateirechte vergeben? | C – Projekt-Workspace + explizite Ordnerfreigaben |
| 15 | Wie wird 16-GB-RAM verwaltet? | D – Smart Memory Manager |
| 16 | Wie werden Modelle ausgewählt? | E – automatischer Benchmark auf dem echten Mac |
| 17 | Welches Sicherheitsniveau gilt? | A+B+C+D+E – Keychain, Login, API-Key, Secret-Filter, Touch ID wo möglich |
| 18 | Wie wird der Altbestand übernommen? | D – Backup -> Analyse -> sauberer Neubau |
| 19 | Wie soll die Installation später aussehen? | D – One-Command + Smart Setup Wizard |
| 20 | Wie arbeiten mehrere Agenten zusammen? | D – Smart Orchestrator |
| 21 | Wie viele Benutzer unterstützt V1? | B – ein Admin, später erweiterbar |
| 22 | Wie werden Projekte indexiert? | D – Smart Project Indexer |
| 23 | Wie wird die App gestartet? | D – native Mac-Launcher-App + lokale Web-App |
| 24 | Wie ist Netzwerkzugriff standardmäßig? | D – localhost; LAN/Remote optional |
| 25 | Wie werden Erweiterungen verwaltet? | D – kuratierter Extension Hub |
| 26 | Was enthält das Admin Center? | A+B+C+D+E – Modelle, Agenten, Skills/MCP, Routing, System Health |
| 27 | Wie werden alte Daten aufbewahrt? | D – Smart Retention |
| 28 | Wie werden Verbesserungen ausgerollt? | D – staged improvement |
| 29 | Wo liegen KITZLABS-Daten? | D – zentral verwalteter KITZLABS Root |
| 30 | Was startet automatisch? | D – nur leichte Kernservices |
| 31 | Welche Abnahmetests sind Pflicht? | A+B+C+D+E – Core, Agents, MCP, Security, Performance |
| 32 | Welche Hauptarchitektur gilt? | B – KITZLABS Control Layer + LocalAI Core |
| 33 | Wie reagiert das System auf Fehler? | D – Autonomous Recovery Engine |
| 34 | Wie wird Recovery abgesichert? | D – Recovery Vault / Restore |
| 35 | Wie lernt das System weiter? | D – kontinuierliches Smart Learning |
| 36 | Wie werden Updates behandelt? | D – autonome staged updates |
| 37 | Wie entstehen neue Fähigkeiten? | D – Autonomous Capability Factory |
| 38 | Wie werden laufende Operationen koordiniert? | D – Autonomous Operations Manager |
| 39 | Wie werden Ressourcen geregelt? | D – Adaptive Resource Governor |
| 40 | Wie werden Aufgaben priorisiert? | D – Intelligent Priority Engine |
| 41 | Wie wird Nachvollziehbarkeit gesichert? | D – vollständiger Audit Trail |
| 42 | Wie werden Secrets verwaltet? | D – Autonomous Secret Vault |
| 43 | Wie arbeitet der Installer? | D – Trusted Autonomous Installer |
| 44 | Wie werden Fähigkeiten/Rechte dynamisch geregelt? | D – Dynamic Capability Policy |
| 45 | Welche Root-Struktur wird verwendet? | D – Managed KITZLABS Root |
| 46 | Wie wird Modell-Cache verwaltet? | D – Smart Model Cache |
| 47 | Wie oft werden Benchmarks neu bewertet? | D – Adaptive Benchmark Scheduler |
| 48 | Wie werden alte Modelle/Daten entfernt? | D – Adaptive Retention |
| 49 | Wie ist der Bootstrap geschützt? | D – Secure Bootstrap Installer |
| 50 | Wie werden alte Modelle migriert? | D – Smart Model Migration |
| 51 | Wie wird Speicherplatz geregelt? | D – Adaptive Storage Governor |
| 52 | Wird Ollama integriert? | B – bleibt installiert, aber nicht integriert |
| 53 | Wie wird Knowledge aktualisiert? | D – Incremental Knowledge Indexer |
| 54 | Welche lokale Datenspeicherung? | D – SQLite + separater Vektorindex |
| 55 | Wie werden lokale Daten verschlüsselt? | D – Smart Local Encryption |
| 56 | Wie funktioniert Autostart? | D – Smart Autostart |
| 57 | Welche Modellquellen sind erlaubt? | D+E – vertrauenswürdige Quellen + direkte Links mit Prüfung |
| 58 | Wie werden schlechte Modelle behandelt? | D – Failover + Quarantine |
| 59 | Welche Privacy-Strategie gilt? | D – local first |
| 60 | Wie wird Apple-Backend ausgewählt? | D – Adaptive Apple Backend Engine |
| 61 | Was passiert bei einem Modell-Link? | D – Link-to-Model Autopilot |
| 62 | Wie werden neue Modelle freigegeben? | D – Autonomous Model Qualification |
| 63 | Welche GitHub-Quelle ist Source of Truth? | D – privates Master-Repo-Konzept |
| 64 | Wie autonom darf GitHub geändert werden? | D – Branch -> Code -> Test -> Commit -> PR |
| 65 | Wie wird CI genutzt? | D – automatische Tests/Security/Build/Release-Checks |
| 66 | Wie werden Issues und PRs behandelt? | D – autonomer Lifecycle |
| 67 | Wie werden externe Repos genutzt? | D – GitHub Intelligence Engine |
| 68 | Wie werden Prompts verwaltet? | D – Autonomous Prompt Intelligence Library |
| 69 | Dürfen neue Prompts automatisch entstehen? | D – ja, testen und speichern |
| 70 | Wie werden Prompts bewertet? | D – Prompt Benchmark Lab |
| 71 | Welche Prompt-Hierarchie gilt? | D – Global + Agent + Projekt + Skill + Task Context |
| 72 | Wie wird der passende Prompt gewählt? | D – Dynamic Prompt Router |
| 73 | Wie wird die Übersichtsseite gestaltet? | E – Mission-Control-Dashboard |
| 74 | Welche Schnellaktionen stehen oben? | E – Neuer Chat, Neue Aufgabe, Agent starten, Projekt öffnen |
| 75 | Welche Statuskarten erscheinen? | E – LocalAI/Modelle, Mac, Agenten/Aufgaben, Verbindungen |
| 76 | Wie werden aktive Agenten dargestellt? | E – vollständige kompakte Agentenkarten |
| 77 | Wie wird autonome Tagesarbeit dargestellt? | E – Tagesprotokoll + Kennzahlen |
| 78 | Wie startet ein neuer Chat? | E – intelligenter Start mit Auto-Routing |
| 79 | Welche Chat-Steuerleiste gilt? | E – Projekt, Agent, Modell, Autonomie, Memory, Tools |
| 80 | Was kann in Chats eingefügt werden? | E – Dateien, Bilder, Ordner, Links mit Auto-Erkennung |
| 81 | Wie autonom arbeitet ein Chat? | E+ – sehr hohe Autonomie innerhalb Freigaben |
| 82 | Wie wird Agentenarbeit im Chat angezeigt? | E – kompakte Live-Timeline |
| 83 | Welche Aktionen hat jede Antwort? | E – vollständige kontextabhängige Aktionsleiste |
| 84 | Dürfen Multi-Agent-Teams automatisch entstehen? | E – ja, KITZ Master orchestriert |
| 85 | Wie arbeitet Chat-Memory? | E – intelligentes Langzeit-/Projekt-/Fehler-/Erfolgs-Memory |

## Änderungsregel

Beispiel: `Q81=C` reduziert die Chat-Autonomie. Danach müssen Policy, UI und Tests für Q81 synchron angepasst werden.
