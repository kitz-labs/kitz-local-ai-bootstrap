# KITZLABS AI Master Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the complete KITZLABS AI Command Center Pro on macOS/Apple Silicon with LocalAI as the inference core, a KITZLABS Control Layer, guarded tool execution, project-aware agents, local memory/knowledge, model routing, connectors, recovery, and a full-screen cockpit.

**Architecture:** The system is split into independently testable subsystems. The Cockpit talks only to the Control Layer. The Control Layer orchestrates agents, memory, projects, tasks, models and events. All tool execution passes through the Tool Gateway and Smart Guard before reaching LocalAI, GitHub, browser/research, MCP/APIs, Telegram or Python apps.

**Tech Stack:** TypeScript/Node.js for Control Layer and Cockpit, SQLite for durable local state, local vector index for RAG, LocalAI HTTP/MCP interfaces, GitHub API, Playwright/Crawl4AI-compatible browser workers, Python/uv for isolated Python apps, macOS Keychain for secrets, Vitest/Playwright for tests.

**Spec:** `docs/architecture/master-design.md` and `docs/architecture/questions-001-085.md` through `questions-247-326.md`

## Global Constraints

- macOS on Apple Silicon with 16 GB Unified Memory is the primary target.
- Local-first by default; cloud providers are explicit/manual only.
- Stable model aliases: `kitz-main`, `kitz-code`, `kitz-fast`, `kitz-embed`.
- Ollama may remain installed but is not part of the architecture.
- Destructive, privileged, secret-sensitive and production-impacting actions must pass Smart Guard.
- Risky changes create a snapshot or Git restore point before activation.
- Personal memory, secrets and model binaries must never be committed to GitHub.
- UI copy is German; product names such as LocalAI, GitHub, Telegram, MCP remain unchanged.
- Each subsystem must have health checks, tests, audit events and a recovery path.

---

## Delivery Order

1. Foundation and repository structure
2. Control Layer core and event bus
3. LocalAI integration and model registry
4. Tool Gateway, Smart Guard and Secret Vault
5. Projects, tasks, scheduler and activity log
6. Agent orchestrator and specialist agents
7. Memory, knowledge, RAG and context intelligence
8. Model router and resource governor
9. GitHub, browser, research, MCP/API and Telegram connectors
10. Python App Operator
11. Cockpit full-screen UI
12. Recovery, Time Machine, backup and root-cause engine
13. Media studios and extension hub
14. Acceptance tests, migration and one-command installer

## Plan Files

- `2026-08-31-plan-01-foundation-control-localai.md`
- `2026-08-31-plan-02-security-projects-agents-memory.md`
- `2026-08-31-plan-03-connectors-python-cockpit.md`
- `2026-08-31-plan-04-recovery-media-installer-acceptance.md`

## Execution Rules for Codex

- [ ] Read `README.md`, `docs/architecture/master-design.md`, and all Q001-Q326 files before implementation.
- [ ] Implement only one task at a time.
- [ ] Start every task with a failing test or an explicit executable validation when a unit test is not suitable.
- [ ] Do not modify unrelated bootstrap/release behavior.
- [ ] Keep files small and responsibility-focused.
- [ ] Commit each independently testable task.
- [ ] Never place secrets in tracked files; use environment references or Keychain adapters.
- [ ] For LocalAI source-level changes, preserve REST/MCP/skill-prompt synchronization rules documented in the architecture.
- [ ] Do not activate a new model, prompt, skill or backend unless benchmark/validation beats or equals the current stable configuration.
- [ ] Record every autonomous mutation in the audit log.

## Definition of Done

The complete system is done only when:

- [ ] A user can open the full-screen KITZLABS cockpit and create/import a project.
- [ ] `kitz-main`, `kitz-code`, `kitz-fast`, and `kitz-embed` resolve to tested local models.
- [ ] KITZ Master can delegate to specialist agents and show live progress.
- [ ] Tools execute only through Tool Gateway + Smart Guard.
- [ ] Project memory, knowledge and semantic retrieval work locally.
- [ ] GitHub, browser/research, MCP/API, Telegram and Python app integrations are visible and testable.
- [ ] Project Time Machine can restore a verified previous state.
- [ ] Secrets never appear in logs, prompts, Git history or UI exports.
- [ ] The system remains within the Mac's resource envelope under normal use.
- [ ] A clean machine can be installed via the documented one-command bootstrap flow.
