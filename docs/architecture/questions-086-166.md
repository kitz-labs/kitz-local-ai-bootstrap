# Fragen Q086–Q166 – Core, Modelle, Agenten, Memory, Skills, MCP

Für alle Fragen in dieser Datei gilt aktuell: **Empfehlung E = Entscheidung E**, sofern später nicht per Fragennummer geändert.

## Antwortschema

- **A** = minimal / nur anzeigen / manuell
- **B** = Basisfunktion mit begrenzter Steuerung
- **C** = erweiterte Funktion mit mehr Integration
- **D** = hochautomatisiert mit Schutzmechanismen
- **E** = ⭐ vollständig integriert, autonom innerhalb freigegebener Grenzen, getestet, versioniert und rücksetzbar

## LocalAI Core Engineer – Q086–Q100

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 86 | Darf der LocalAI-Entwickler LocalAI-Konfigurationen lesen und ändern? | E – vollständig, mit Snapshot und Tests |
| 87 | Darf er Modell-YAMLs, Aliase und Rollen erzeugen/ändern/löschen? | E – vollständig mit Validierung |
| 88 | Darf er LocalAI-Backends installieren, wechseln und konfigurieren? | E – ja, kompatibilitätsgeprüft |
| 89 | Darf er LocalAI-Go-Quellcode ändern? | E – ja, nur über Branch/Worktree + Tests |
| 90 | Darf er REST-Endpunkte erweitern? | E – ja, inklusive synchroner MCP-/Skill-Anpassung |
| 91 | Darf er LocalAI-MCP-Tools erweitern? | E – ja, REST/MCP/Prompt-Layer synchron halten |
| 92 | Darf er LocalAI Assistant und System-Prompts ändern? | E – versioniert + Benchmark + Rollback |
| 93 | Darf er Web-UI und CLI von LocalAI anpassen? | E – ja, mit UI/CLI-Tests |
| 94 | Darf er Metal-/Apple-Backend-Einstellungen optimieren? | E – autonom nach Benchmark |
| 95 | Darf er LocalAI bauen, starten, stoppen und neu starten? | E – ja, mit Health-Check und Recovery |
| 96 | Darf er Versionen upgraden/downgraden? | E – staged, mit Snapshot und Rückfallpunkt |
| 97 | Wie werden Änderungen an LocalAI isoliert? | E – privater Fork + Feature-Branch/Worktree |
| 98 | Wie werden LocalAI-Änderungen geprüft? | E – Build, Unit, Integration, Smoke, Model, Agent, Performance |
| 99 | Was passiert bei fehlgeschlagenen LocalAI-Änderungen? | E – automatische Diagnose + Rollback/Quarantäne |
| 100 | Wie arbeitet der sichtbare LocalAI-Entwickler intern? | E – Mini-Team aus Core, Models, Agent/MCP, UI, QA nach Bedarf |

## Modelle / Routing / Hugging Face – Q101–Q112

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 101 | Wie werden neue Modelle gefunden? | E – Hugging Face + direkte Links + vertrauenswürdige Quellen |
| 102 | Wie wird die richtige Datei/Quantisierung gewählt? | E – automatisch nach RAM, Metal, Kontext und Aufgabe |
| 103 | Wie wird Modell-Kompatibilität mit 16 GB geprüft? | E – Preflight + Speicherprognose + Testload |
| 104 | Wie werden Modelle installiert? | E – Download -> Verify -> Register -> Benchmark -> Role |
| 105 | Wie werden Rollen `kitz-main/code/fast/embed` vergeben? | E – Benchmark-basiert |
| 106 | Wie wird zur Laufzeit zwischen Modellen gewechselt? | E – Adaptive Model Router |
| 107 | Wie werden große Modelle behandelt? | E – dynamisches Load/Unload nach Ressourcenlage |
| 108 | Wie werden schlechte oder instabile Modelle behandelt? | E – Quarantine + Failover |
| 109 | Wie werden Modelle aktualisiert? | E – staged Update + Vergleichsbenchmark |
| 110 | Wie werden Modellversionen dokumentiert? | E – Registry mit Quelle, Hash, Quantisierung, Rolle, Score |
| 111 | Wie wird Hugging Face im Cockpit dargestellt? | E – eigene Modellzentrale + Projektkarte + Live-Status |
| 112 | Wie werden Modell-Empfehlungen verbessert? | E – echte lokale Benchmarks + Nutzungsmetriken |

## Agenten / Teams / Rechte – Q113–Q124

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 113 | Wer ist Standard-Einstieg für komplexe Aufgaben? | E – KITZ Master |
| 114 | Wie wählt der Master Spezialagenten? | E – automatisch nach Aufgabe, Skills, Tools und Modell |
| 115 | Dürfen Agenten parallel arbeiten? | E – ja, wenn Aufgaben unabhängig sind |
| 116 | Wie werden Agentenrechte vergeben? | E – projektbezogene Capability Policy |
| 117 | Dürfen Agenten Unteraufgaben erzeugen? | E – ja, inklusive Priorisierung |
| 118 | Dürfen Agenten weitere Agenten starten? | E – ja, ressourcen- und policy-gesteuert |
| 119 | Wie werden Agenten bewertet? | E – Erfolgsquote, Qualität, Geschwindigkeit, Kosten/RAM, Fehler |
| 120 | Wie werden Agenten verbessert? | E – Prompt/Skill/Tool-Routing mit Benchmark und Rollback |
| 121 | Wie werden fehlgeschlagene Agenten ersetzt? | E – Failover auf passenden Spezialagenten |
| 122 | Wie sieht die Agenten-Zentrale aus? | E – Karten mit Status, Aufgabe, Modell, Tools, Autonomie, Verlauf |
| 123 | Wie werden Agenten-Teams dargestellt? | E – Teamansicht mit Leader, Worker, Fortschritt und Abhängigkeiten |
| 124 | Wie wird Ressourcenverbrauch von Agenten begrenzt? | E – Adaptive Resource Governor |

## Memory / Wissen / RAG / Knowledge Graph – Q125–Q134

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 125 | Welche Memory-Ebenen gibt es? | E – persönlich, Projekt, Fehler/Lösung, Erfolgsmuster, temporär |
| 126 | Was wird automatisch gespeichert? | E – nur relevante, deduplizierte und bewertete Erkenntnisse |
| 127 | Wie werden widersprüchliche Erinnerungen behandelt? | E – Versionierung + Aktualitäts-/Vertrauensbewertung |
| 128 | Wie werden alte Erinnerungen behandelt? | E – zusammenfassen, ersetzen oder nach Retention archivieren |
| 129 | Wie wird Projektwissen aufgebaut? | E – inkrementelle Indexierung aus Dateien, Code, Web, GitHub, Docs |
| 130 | Wie wird RAG-Kontext ausgewählt? | E – Context Intelligence statt blindem Vollindex |
| 131 | Welche Datenspeicherung wird genutzt? | E – SQLite Metadaten + lokaler Vektorindex |
| 132 | Wie wird Knowledge Graph erzeugt? | E – automatisch aus Entitäten und Beziehungen |
| 133 | Wie werden Quellen nachvollziehbar gemacht? | E – Source-Metadaten + Pfad/URL + Zeit + Version |
| 134 | Wie wird sensibles Wissen geschützt? | E – Verschlüsselung + Projektgrenzen + Secret-Filter |

## Skills / Prompts / autonome Verbesserung – Q135–Q144

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 135 | Wie werden vorhandene Skills gefunden? | E – Skill Scout über geprüfte Kataloge/GitHub |
| 136 | Dürfen Skills automatisch importiert werden? | E – nur nach Security-, Sandbox- und Benchmark-Prüfung |
| 137 | Dürfen neue Skills autonom entstehen? | E – aus wiederholten erfolgreichen Mustern |
| 138 | Wie werden Skills versioniert? | E – Git + Metadaten + Tests + Rollback |
| 139 | Wie sind Prompts hierarchisch aufgebaut? | E – Global + Agent + Projekt + Skill + Task Context |
| 140 | Dürfen Prompts automatisch verbessert werden? | E – ja, über Prompt Benchmark Lab |
| 141 | Wie werden Prompt-Versionen aktiviert? | E – Shadow/Canary, nur bessere Version aktivieren |
| 142 | Wie werden Prompts/Skills im UI verwaltet? | E – Bibliothek mit Suche, Score, Version, Agent/Projekt-Zuordnung |
| 143 | Wie werden schlechte Verbesserungen behandelt? | E – automatischer Rollback |
| 144 | Wie wird verhindert, dass Sicherheit wegoptimiert wird? | E – unveränderlicher Safety Core außerhalb Selbstoptimierung |

## MCP / APIs / Connector Center – Q145–Q154

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 145 | Wie werden MCP-Server verwaltet? | E – zentrale MCP-Zentrale mit Health, Rechten und Projektzuordnung |
| 146 | Wie werden APIs gefunden? | E – API Scout mit Katalogsuche und Prüfung |
| 147 | Wie werden API-Authentifizierung und Secrets gespeichert? | E – Secret Vault/Keychain, nie in Prompts/Knowledge |
| 148 | Wie werden neue Connectoren getestet? | E – Sandbox + Schema-Test + Probe-Call |
| 149 | Wie werden Connector-Rechte begrenzt? | E – pro Projekt/Agent/Capability |
| 150 | Wie werden ausgefallene Connectoren behandelt? | E – Health Check + Retry + Failover + Alarm |
| 151 | Wie werden MCP/API-Aktionen auditiert? | E – vollständiger Audit Trail |
| 152 | Wie wählt ein Agent zwischen mehreren Tools? | E – Tool Router nach Fähigkeit, Sicherheit und Erfolgsrate |
| 153 | Wie werden GitHub, Browser, Telegram und Notion integriert? | E – als getrennte Connectoren hinter demselben Tool Gateway |
| 154 | Wie sieht die Connector-Zentrale aus? | E – Statuskarten, Rechte, Secrets, Test, Logs, Projektzuordnung |

## Projektseite / Vollbild-Cockpit – Q155–Q166

| Q | Frage | ⭐ Empfehlung / aktuelle Entscheidung |
|---:|---|---|
| 155 | Nutzt die App die gesamte Browserfläche? | E – ja, Vollbild ohne unnötige Außenränder |
| 156 | Wie verhält sich die linke Navigation? | E – Smart Sidebar, breit/Icons/automatisch kompakt |
| 157 | Wie verhält sich die rechte Live-Leiste? | E – offen/kompakt/versteckt je nach Platz |
| 158 | Bleibt der Projektkopf sichtbar? | E – Sticky Header |
| 159 | Sind Dashboard-Karten frei anpassbar? | E – Drag, Resize, Hide, projektweise speichern |
| 160 | Welche Schnellaktionen stehen im Projektkopf? | E – Chat, Aufgabe, Agent, Autopilot, Diagnose, GitHub, HF |
| 161 | Wie ist der obere KPI-Bereich? | E – Health, Aufgaben, Agenten, Fehler, GitHub, Modelle |
| 162 | Was steht direkt unter den KPIs? | E – Aktive Arbeit + Warnungen/Nächste Schritte |
| 163 | Was steht im mittleren Bereich? | E – Aufgaben + Dateien + GitHub + Wissen/Modelle |
| 164 | Was steht unten? | E – Aktivitäten + Zeitmaschine |
| 165 | Wie wird Autopilot im Projekt gesteuert? | E – vollständiges Panel mit Rechten, Tools, Jobs und Verlauf |
| 166 | Wie werden Layouts gespeichert? | E – pro Projekt + Default-Layout + Reset |

## Änderungsbeispiel

`Q107=C` würde das automatische Load/Unload großer Modelle reduzieren. Die Änderung muss anschließend in Model Router, Ressourcenregeln, UI und Tests übernommen werden.
