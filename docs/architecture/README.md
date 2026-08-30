# KITZLABS AI – Architektur-Entscheidungen

Stand: 2026-08-30

Diese Dokumentation ist die zentrale Entscheidungsquelle für den KITZLABS AI / LocalAI Neubau.

## Regel

- Jede Entscheidung hat eine eindeutige Fragennummer `Q...`.
- `E` ist standardmäßig die empfohlene und aktuell gesetzte Variante, sofern nicht ausdrücklich anders dokumentiert.
- Änderungen werden immer über die Fragennummer vorgenommen, z. B. `Q176=C`.
- Eine geänderte Entscheidung muss anschließend in Architektur, Tests und Implementierungsplan synchronisiert werden.
- Sicherheitskern, Secret-Schutz, Snapshots und Rollback dürfen nicht durch eine normale Projektentscheidung abgeschaltet werden.

## Dateien

- `questions-001-085.md` – bereits gemeinsam entschiedene Grundarchitektur und UI
- `questions-086-166.md` – LocalAI, Modelle, Agenten, Memory, Skills, MCP
- `questions-167-246.md` – Browser, Python, GitHub, Telegram, Workflows, Security, Recovery
- `questions-247-326.md` – System, Medien, Dateien, Installation, Updates, UI, Monitoring, Tests
- `master-design.md` – konsolidierte Zielarchitektur

## Zielarchitektur in einem Satz

Vollbild-KITZLABS-Cockpit -> KITZLABS Control Layer -> Smart Guard / Tool Gateway -> LocalAI Core + Agenten + MCP/API/Browser/GitHub/Telegram/Python -> lokale Daten-, Memory-, Knowledge-, Backup- und Benchmark-Schicht.

## Standard-Autonomie

Maximale Autonomie innerhalb explizit freigegebener Projektgrenzen. Kritische Systemrechte, Secret-Offenlegung, irreversible Löschungen und produktionskritische Aktionen bleiben geschützt oder benötigen eine Freigabe.
