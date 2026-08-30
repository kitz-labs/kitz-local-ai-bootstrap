# Fragen Q167–Q246 – Browser, Python, GitHub, Telegram, Workflows, Security, Recovery

Für alle Fragen gilt aktuell: **Empfehlung E = Entscheidung E**.

## Antwortschema

- **A** minimal/manuell
- **B** Basis
- **C** erweitert
- **D** hochautomatisiert
- **E** ⭐ vollständig integriert, autonom in freigegebenen Grenzen, getestet und rücksetzbar

## Browser / Research / Scraping – Q167–Q174

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 167 | Wie wird Browser-Automation genutzt? | E – Browser Agent Center mit kontrollierten Sessions |
| 168 | Welche Browser-Engine ist Standard? | E – Playwright für deterministische Automation, Browser-Agent bei komplexen Aufgaben |
| 169 | Wie werden Webseiten für RAG extrahiert? | E – Crawl4AI/strukturierte Extraktion mit Quellen |
| 170 | Dürfen Agenten autonome Web-Recherchen durchführen? | E – ja, mehrquellig und nachvollziehbar |
| 171 | Wie werden Scraping-Jobs geplant? | E – Task/Scheduler integriert |
| 172 | Wie werden Website-Änderungen überwacht? | E – wiederkehrende Checks mit Diff und Triggern |
| 173 | Wie werden Web-Ergebnisse ins Wissen übernommen? | E – nur relevante, deduplizierte Inhalte mit Quelle |
| 174 | Wie werden fehlerhafte/gesperrte Seiten behandelt? | E – alternative Quelle/Engine, sauberer Fehlerstatus |

## Python App Operator – Q175–Q182

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 175 | Wie werden Python-Anwendungen gefunden? | E – Scan explizit freigegebener Ordner |
| 176 | Wie wird der Startbefehl erkannt? | E – Analyse von pyproject, requirements, README, entrypoints und bekannten Mustern |
| 177 | Wie werden Python-Umgebungen isoliert? | E – eigene uv-Umgebung pro App |
| 178 | Welche App-Aktionen gibt es? | E – Start, Stop, Restart, Logs, Open, Repair |
| 179 | Wie werden fehlende Abhängigkeiten behandelt? | E – isoliert prüfen/installieren, keine globale Blindinstallation |
| 180 | Wie werden Startbefehle gemerkt? | E – nur verifizierte Befehle als App-Metadaten speichern |
| 181 | Was passiert bei App-Absturz? | E – Root Cause, Repair, Retry, ggf. Rollback |
| 182 | Wie sieht die Python-App-Seite aus? | E – Karten/Tabelle mit Status, Aktionen, Logs, Umgebung und Health |

## GitHub Intelligence – Q183–Q190

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 183 | Wie wird GitHub pro Projekt angebunden? | E – Repo-Zuordnung im Projekt-Hub |
| 184 | Dürfen Agenten Branches und Commits erstellen? | E – ja, automatisch innerhalb Projektregeln |
| 185 | Dürfen Agenten PRs und Issues erzeugen/pflegen? | E – ja, mit Audit und Status |
| 186 | Wie wird CI ausgewertet? | E – Actions/Checks analysieren, Fehler automatisch klassifizieren |
| 187 | Dürfen fehlgeschlagene CI-Jobs neu gestartet werden? | E – ja, nach Ursache und Policy |
| 188 | Wie werden öffentliche Repos als Wissensquelle genutzt? | E – GitHub Intelligence mit Trust/Security/Sandbox |
| 189 | Wie werden Upstream-Änderungen verfolgt? | E – Diff/Release/Commit Intelligence |
| 190 | Wie sieht die GitHub-Zentrale aus? | E – Changes, Branches, Issues, PRs, Actions, Agentenaktivität |

## Telegram Gateway – Q191–Q196

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 191 | Wie wird Telegram angebunden? | E – eigener Gateway/Connector |
| 192 | Dürfen Agenten Nachrichten senden und empfangen? | E – ja, nur für freigegebene Bots/Chats |
| 193 | Können Telegram-Nachrichten Aufgaben auslösen? | E – ja, über Trigger/Intent |
| 194 | Können Agenten Status/Ergebnisse nach Telegram senden? | E – ja, mit kompakten sicheren Zusammenfassungen |
| 195 | Wie werden Telegram-Tokens gespeichert? | E – ausschließlich Secret Vault/Keychain |
| 196 | Wie wird Telegram im Projekt angezeigt? | E – Bot-Status, Chats, Trigger, Workflows, Logs |

## Workflow Builder / Scheduler / Tasks – Q197–Q206

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 197 | Wie werden Workflows gebaut? | E – visueller Builder + agentische Erstellung |
| 198 | Welche Trigger werden unterstützt? | E – Zeit, Datei, GitHub, API, Fehler, Webhook, Systemzustand |
| 199 | Welche Aktionen dürfen Workflows ausführen? | E – Agenten, Tools, APIs, Python, GitHub, Browser, LocalAI |
| 200 | Dürfen erfolgreiche Abläufe automatisch zu Workflows werden? | E – ja, nach Test/Validierung |
| 201 | Wie werden Workflow-Versionen verwaltet? | E – versioniert + diff + rollback |
| 202 | Wie werden geplante Aufgaben dargestellt? | E – Liste, Kalender, nächste Läufe, Status |
| 203 | Wie werden blockierte Aufgaben behandelt? | E – Abhängigkeiten erkennen und neu priorisieren |
| 204 | Wie werden lange Aufgaben zerlegt? | E – Unteraufgaben mit Orchestrierung |
| 205 | Wie werden Task-Ergebnisse dokumentiert? | E – Abschlussbericht + Artefakte + Memory/Knowledge |
| 206 | Wie werden wiederkehrende Fehler in Tasks behandelt? | E – Recovery Loop + Root Cause + Eskalationsgrenze |

## Security / Smart Guard / Secret Vault – Q207–Q216

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 207 | Wie werden Secrets gespeichert? | E – Keychain/Secret Vault, nie Klartext in Repo/Memory |
| 208 | Wie werden Secret-Leaks verhindert? | E – Input/Output/Log-Filter + Redaction |
| 209 | Wie werden Projektberechtigungen definiert? | E – explizite Projektgrenzen + Capability Policy |
| 210 | Welche Aktionen benötigen Freigabe? | E – nur kritische/irreversible/außerhalb erlaubter Grenzen |
| 211 | Können Freigaben dauerhaft pro Projekt gesetzt werden? | E – ja, granular und widerrufbar |
| 212 | Wo wird Touch ID genutzt? | E – kritische Freigaben, soweit technisch möglich |
| 213 | Wie wird der Safety Core geschützt? | E – unveränderliche Mindestregeln außerhalb Selbstoptimierung |
| 214 | Wie werden lokale API-Zugriffe geschützt? | E – lokale Auth/API-Key + least privilege |
| 215 | Wie werden Rechteänderungen protokolliert? | E – unveränderbarer Audit Trail |
| 216 | Wie sieht das Security Center aus? | E – Secrets, Rechte, Freigaben, Audit, Risiken, Sessions |

## Recovery / Backups / Zeitmaschine / Root Cause – Q217–Q224

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 217 | Wann werden Snapshots erstellt? | E – vor relevanten Änderungen automatisch |
| 218 | Welche Ebenen sind wiederherstellbar? | E – Datei, Config, Prompt, Skill, Agent, Projekt, Systemstand |
| 219 | Wie werden stabile Stände markiert? | E – nach erfolgreichen Tests/Health Checks automatisch |
| 220 | Wann wird automatisch zurückgerollt? | E – bei fehlgeschlagenen Tests, Health-Regressions oder Startfehlern |
| 221 | Wie funktioniert Root Cause Analysis? | E – Logs + Code + Git + Memory + Systemzustand zusammenführen |
| 222 | Wie viele Reparaturversuche sind erlaubt? | E – adaptiv, aber mit Eskalationsgrenze gegen Endlosschleifen |
| 223 | Wie wird Backup-Retention gesteuert? | E – Smart Retention nach Alter, Wichtigkeit und Speicherplatz |
| 224 | Wie sieht die Zeitmaschine aus? | E – Timeline, Vergleich, Einzel-Restore, kompletter Rollback |

## System Health / Ressourcen – Q225–Q232

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 225 | Welche Mac-Metriken werden überwacht? | E – RAM, CPU, Storage, Last, Prozesse, verfügbare relevante Sensoren |
| 226 | Wie wird Metal-Status überwacht? | E – Backend/Device/Load-Checks |
| 227 | Wie werden Modell-Ressourcen priorisiert? | E – Resource Governor nach Aufgabe und Priorität |
| 228 | Was passiert bei RAM-Druck? | E – Modelle entladen, Jobs drosseln, Prioritäten anwenden |
| 229 | Wie werden Hintergrundaufgaben behandelt? | E – nur bei ausreichenden Ressourcen |
| 230 | Wie werden Systemdienste überwacht? | E – Health Checks + Restart/Recovery |
| 231 | Wie werden Prozesse/Ports sichtbar gemacht? | E – System Map + Health Center |
| 232 | Wie sieht die rechte Live-Bar aus? | E – Mac, LocalAI, Metal, Modelle, Agenten, Tasks, Connectoren |

## File Intelligence – Q233–Q238

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 233 | Welche Dateien werden verstanden? | E – Text, Code, PDF, DOCX, PPTX, XLSX/CSV, Bilder/weitere unterstützte Formate |
| 234 | Wie werden Office/PDF-Dateien für LLMs normalisiert? | E – strukturierte Markdown-/Text-Extraktion, z. B. MarkItDown wo passend |
| 235 | Wie wird Dateizugriff begrenzt? | E – nur freigegebene Projektpfade |
| 236 | Wie werden Dateiänderungen erkannt? | E – Event Bus/File Watcher |
| 237 | Welche Dateiaktionen gibt es im UI? | E – Vorschau, Editor, Diff, Agent fragen, reparieren, Wissen übernehmen |
| 238 | Wie werden Binärdateien/ungeeignete Inhalte behandelt? | E – Typprüfung, sichere Vorschau, kein blindes Parsen |

## Connector-/Event-Automation – Q239–Q246

| Q | Frage | ⭐ Empfehlung / Entscheidung |
|---:|---|---|
| 239 | Wie werden Dateiänderungen zu Events? | E – Watchfiles/Event Bus |
| 240 | Können Events Agenten/Workflows starten? | E – ja, regelbasiert |
| 241 | Wie werden Event-Dubletten verhindert? | E – Debounce/Dedupe |
| 242 | Wie werden Event-Fehler behandelt? | E – Retry + Dead-Letter/Fehlerstatus |
| 243 | Wie werden externe Webhooks behandelt? | E – authentifiziert, validiert, projektgebunden |
| 244 | Wie werden Events auditiert? | E – vollständige Timeline |
| 245 | Wie werden Ereignisregeln konfiguriert? | E – UI + Policy-Dateien |
| 246 | Wie verhindert man Event-Schleifen? | E – Herkunfts-ID, Rate Limits, Loop Detection |
