# Recovery, Media, Installer and Acceptance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Finish recovery, root-cause analysis, media studios, extensions, migration, installer and acceptance testing so the complete system is safe to operate and reproducibly installable.

**Architecture:** Recovery is snapshot-first and auditable. Media workloads use queued jobs behind the resource governor. Installation detects existing LocalAI assets, migrates only verified data, and never overwrites secrets or user data without a recoverable backup.

**Tech Stack:** TypeScript/Node.js, SQLite, filesystem snapshots/Git restore points, Python/uv workers where needed, shell wrappers for macOS bootstrap, Vitest and Playwright.

**Spec:** `docs/architecture/master-design.md`

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Snapshot and Time Machine service

**Files:**
- Create: `control-layer/src/recovery/snapshot-service.ts`
- Create: `control-layer/src/recovery/restore-service.ts`
- Test: `control-layer/test/recovery/snapshot-service.test.ts`

**Interfaces:**
- Produces: `createSnapshot`, `listSnapshots`, `diffSnapshot`, `restoreSnapshot`.

- [ ] Write fixture tests proving file restore is exact.
- [ ] Store snapshot metadata in SQLite and payloads under runtime `backups/`.
- [ ] Capture Git commit/branch metadata where applicable.
- [ ] Require Smart Guard evaluation before destructive restore.
- [ ] Commit.

### Task 2: Autonomous recovery and root-cause engine

**Files:**
- Create: `control-layer/src/recovery/root-cause.ts`
- Create: `control-layer/src/recovery/recovery-engine.ts`
- Test: `control-layer/test/recovery/recovery-engine.test.ts`

**Interfaces:**
- Consumes errors, logs, recent changes, task history and snapshots.
- Produces diagnosis, candidate fix, validation result and rollback decision.

- [ ] Test known fixture failure -> proposed fix -> validation success.
- [ ] Test failed repair triggers rollback.
- [ ] Prevent repeated infinite repair loops with attempt limits and fingerprints.
- [ ] Persist successful repairs into error/success memory.
- [ ] Commit.

### Task 3: Backup retention policy

**Files:**
- Create: `control-layer/src/recovery/retention.ts`
- Test: `control-layer/test/recovery/retention.test.ts`

- [ ] Test keep rules for recent, daily, weekly and pinned snapshots.
- [ ] Never delete the last verified stable snapshot.
- [ ] Add dry-run output before cleanup execution.
- [ ] Commit.

### Task 4: Prompt and Skill lifecycle

**Files:**
- Create: `control-layer/src/prompts/prompt-registry.ts`
- Create: `control-layer/src/prompts/benchmark.ts`
- Create: `control-layer/src/skills/skill-registry.ts`
- Create: `control-layer/src/skills/qualification.ts`
- Test: `control-layer/test/prompts/prompt-benchmark.test.ts`
- Test: `control-layer/test/skills/qualification.test.ts`

- [ ] Test versioning and active-version rollback.
- [ ] Require benchmark evidence before automatic promotion.
- [ ] Add skill source, permissions, test status and score metadata.
- [ ] Reject skills requesting capabilities outside policy without explicit grant.
- [ ] Commit.

### Task 5: Extension Hub

**Files:**
- Create: `control-layer/src/extensions/extension-registry.ts`
- Create: `control-layer/src/extensions/sandbox-evaluator.ts`
- Test: `control-layer/test/extensions/extension-registry.test.ts`

- [ ] Test install candidate -> sandbox result -> approved activation flow.
- [ ] Store source URL/revision and checksum.
- [ ] Keep untrusted/failed candidates disabled.
- [ ] Commit.

### Task 6: Resource governor and queued heavy jobs

**Files:**
- Create: `control-layer/src/system/resource-governor.ts`
- Create: `control-layer/src/jobs/job-queue.ts`
- Test: `control-layer/test/system/resource-governor.test.ts`

**Interfaces:**
- Produces admission decision for model loads, agent concurrency, image/video jobs and benchmarks.

- [ ] Test 16 GB policy prevents simultaneous conflicting heavy workloads.
- [ ] Prefer unload/reload rather than leaving large inactive models resident.
- [ ] Add queue priority and cancellation.
- [ ] Commit.

### Task 7: Local image studio backend

**Files:**
- Create: `control-layer/src/media/image-service.ts`
- Create: `control-layer/src/media/media-model-registry.ts`
- Test: `control-layer/test/media/image-service.test.ts`

- [ ] Test queued image request with fake worker.
- [ ] Store outputs under project-scoped runtime media folder.
- [ ] Record model, prompt preset and generation metadata without secrets.
- [ ] Integrate with resource governor.
- [ ] Commit.

### Task 8: Local video studio backend

**Files:**
- Create: `control-layer/src/media/video-service.ts`
- Test: `control-layer/test/media/video-service.test.ts`

- [ ] Test queue and cancellation with fake long-running worker.
- [ ] Enforce stricter resource admission than image jobs.
- [ ] Add progress events for Cockpit.
- [ ] Commit.

### Task 9: Media Cockpit pages

**Files:**
- Create: `cockpit/app/image-studio/page.tsx`
- Create: `cockpit/app/video-studio/page.tsx`
- Test: `cockpit/e2e/media-studios.spec.ts`

- [ ] Write navigation and submit-job E2E tests.
- [ ] Show model, queue, progress, output and project destination.
- [ ] Commit.

### Task 10: Existing-installation scanner and migration planner

**Files:**
- Create: `installer/src/scan-existing.ts`
- Create: `installer/src/migration-plan.ts`
- Test: `installer/test/migration-plan.test.ts`

**Interfaces:**
- Detects current LocalAI install, verified models, existing runtime data and optional Ollama caches without integrating Ollama.

- [ ] Write fixture tests for empty, clean LocalAI and mixed legacy installations.
- [ ] Produce a read-only migration plan before changes.
- [ ] Never migrate unknown config/secrets blindly.
- [ ] Commit.

### Task 11: Safe migration executor

**Files:**
- Create: `installer/src/migrate.ts`
- Test: `installer/test/migrate.test.ts`

- [ ] Test snapshot-before-migrate behavior.
- [ ] Copy verified reusable model/data assets into managed locations.
- [ ] Generate migration report with imported/skipped/quarantined items.
- [ ] Verify rollback restores pre-migration state.
- [ ] Commit.

### Task 12: One-command macOS bootstrap

**Files:**
- Create: `installer/install.sh`
- Create: `installer/src/preflight.ts`
- Create: `installer/src/install.ts`
- Test: `installer/test/preflight.test.ts`

**Interfaces:**
- Bootstrap performs preflight -> dependency verification -> runtime directories -> LocalAI/control/cockpit setup -> health tests -> summary.

- [ ] Test preflight parsing for Apple Silicon, disk space and memory.
- [ ] Make `install.sh` a thin launcher; keep logic testable in TypeScript.
- [ ] Do not require Docker unless a selected optional component needs it.
- [ ] Do not overwrite an existing healthy install without migration path.
- [ ] Commit.

### Task 13: Autostart and launcher integration

**Files:**
- Create: `installer/launchd/ai.kitzlabs.control.plist.template`
- Create: `installer/launchd/ai.kitzlabs.cockpit.plist.template`
- Create: `installer/src/autostart.ts`
- Test: `installer/test/autostart.test.ts`

- [ ] Test rendered plist paths and arguments.
- [ ] Autostart only lightweight required services; heavy models load on demand.
- [ ] Provide uninstall/disable path.
- [ ] Commit.

### Task 14: End-to-end acceptance suite

**Files:**
- Create: `tests/acceptance/core.spec.ts`
- Create: `tests/acceptance/agents.spec.ts`
- Create: `tests/acceptance/security.spec.ts`
- Create: `tests/acceptance/recovery.spec.ts`
- Create: `tests/acceptance/performance.spec.ts`

- [ ] Verify Cockpit -> Control Layer -> LocalAI chat round trip.
- [ ] Verify KITZ Master delegates a coding fixture task and records timeline.
- [ ] Verify forbidden path/system mutation is blocked by Smart Guard.
- [ ] Verify secret values never appear in audit/log output.
- [ ] Verify snapshot -> mutation -> restore round trip.
- [ ] Verify resource governor blocks conflicting heavy workloads.
- [ ] Verify LocalAI outage produces degraded UI state and recovery guidance.
- [ ] Commit.

### Task 15: Release gate

- [ ] Run all workspace unit tests.
- [ ] Run all Cockpit Playwright tests.
- [ ] Run installer tests.
- [ ] Run acceptance suite on target Apple Silicon Mac.
- [ ] Capture benchmark baseline for response latency, memory use and model switch time.
- [ ] Verify `git grep` finds no committed tokens/secrets.
- [ ] Verify clean install and migration install paths separately.
- [ ] Update README status from architecture-only to implemented only after all gates pass.
- [ ] Tag first production-ready release only after acceptance passes.
