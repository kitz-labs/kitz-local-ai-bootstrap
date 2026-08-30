# Security, Projects, Agents and Memory Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add guarded execution, projects, tasks, agents, local memory/knowledge and autonomous context selection.

**Architecture:** Every state-changing action goes through a capability decision. Projects define allowed roots and connectors. Agents receive only project-scoped context and tools. Memory is split into personal, project, success/error and knowledge stores with local retrieval.

**Tech Stack:** TypeScript, SQLite, Zod, macOS Keychain adapter, local vector index, Vitest.

**Spec:** `docs/architecture/master-design.md`

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Capability policy and Smart Guard

**Files:**
- Create: `control-layer/src/security/capabilities.ts`
- Create: `control-layer/src/security/smart-guard.ts`
- Test: `control-layer/test/security/smart-guard.test.ts`

**Interfaces:**
- Produces: `evaluateAction(action, context)` returning `allow | confirm | deny` plus reason code.

- [ ] Write tests for safe project read, project file edit, sudo/system-wide mutation, large delete and secret export.
- [ ] Implement default-deny for unknown capabilities.
- [ ] Add per-project persistent grants for safe repeated actions.
- [ ] Record decisions in audit log.
- [ ] Commit.

### Task 2: Secret Vault adapter

**Files:**
- Create: `control-layer/src/security/secret-vault.ts`
- Create: `control-layer/src/security/keychain-adapter.ts`
- Test: `control-layer/test/security/secret-vault.test.ts`

**Interfaces:**
- Produces: `setSecret(ref, value)`, `getSecret(ref)`, `deleteSecret(ref)`, `listSecretRefs()`.

- [ ] Write tests using an in-memory adapter.
- [ ] Ensure list returns references only, never values.
- [ ] Add macOS Keychain runtime adapter.
- [ ] Add log redaction utility and tests.
- [ ] Commit.

### Task 3: Project service and allowed roots

**Files:**
- Create: `control-layer/src/projects/project-service.ts`
- Create: `control-layer/src/projects/project-repository.ts`
- Test: `control-layer/test/projects/project-service.test.ts`

**Interfaces:**
- Produces: `createProject`, `importProject`, `grantRoot`, `revokeRoot`, `getProjectHealth`.

- [ ] Write tests proving file roots are canonicalized and cannot escape by `..` or symlink traversal.
- [ ] Store explicit allowed roots in SQLite.
- [ ] Add import metadata fields for stack, Git repo, start/test commands and detected services.
- [ ] Commit.

### Task 4: Project indexer

**Files:**
- Create: `control-layer/src/projects/indexer/file-filter.ts`
- Create: `control-layer/src/projects/indexer/indexer.ts`
- Test: `control-layer/test/projects/indexer.test.ts`

**Interfaces:**
- Produces incremental file inventory while excluding `.git`, node modules, model binaries, secret/env files and configured ignores.

- [ ] Write exclusion tests first.
- [ ] Add change fingerprinting so unchanged files are skipped.
- [ ] Emit file-index events.
- [ ] Commit.

### Task 5: Task system and priority engine

**Files:**
- Create: `control-layer/src/tasks/task-service.ts`
- Create: `control-layer/src/tasks/priority-engine.ts`
- Test: `control-layer/test/tasks/task-service.test.ts`

**Interfaces:**
- Task states: `open`, `running`, `review`, `blocked`, `done`, `failed`, `cancelled`.
- Produces: create/update/claim/complete/retry operations.

- [ ] Test valid and invalid state transitions.
- [ ] Add deterministic priority score from urgency, impact, dependency blocking and user pinning.
- [ ] Emit activity events for transitions.
- [ ] Commit.

### Task 6: Scheduler and trigger model

**Files:**
- Create: `control-layer/src/automation/scheduler.ts`
- Create: `control-layer/src/automation/triggers.ts`
- Test: `control-layer/test/automation/scheduler.test.ts`

**Interfaces:**
- Trigger types: time, file-change, GitHub event, API event, error event, condition.

- [ ] Write tests for due scheduling and duplicate suppression.
- [ ] Store schedules durably.
- [ ] Ensure a crashed process can resume without double-running completed jobs.
- [ ] Commit.

### Task 7: Agent registry and role definitions

**Files:**
- Create: `control-layer/src/agents/agent-registry.ts`
- Create: `agents/kitz-master/agent.yaml`
- Create: `agents/coding-pro/agent.yaml`
- Create: `agents/research/agent.yaml`
- Create: `agents/mac-operator/agent.yaml`
- Create: `agents/devops/agent.yaml`
- Create: `agents/localai-developer/agent.yaml`
- Create: `agents/python-app-operator/agent.yaml`
- Test: `control-layer/test/agents/agent-registry.test.ts`

**Interfaces:**
- Produces validated agent definitions containing role, model role, tools, default autonomy and system-prompt reference.

- [ ] Write schema tests.
- [ ] Register all seven visible agents.
- [ ] Ensure LocalAI Developer cannot disable Smart Guard or audit.
- [ ] Commit.

### Task 8: Agent orchestrator

**Files:**
- Create: `control-layer/src/agents/orchestrator.ts`
- Create: `control-layer/src/agents/delegation-policy.ts`
- Test: `control-layer/test/agents/orchestrator.test.ts`

**Interfaces:**
- Produces: `runAgentTask`, `delegate`, `pauseRun`, `cancelRun`, `getRunTimeline`.

- [ ] Test single-agent execution.
- [ ] Test KITZ Master delegation to coding/research workers.
- [ ] Bound concurrent workers by resource governor interface.
- [ ] Persist run timeline and tool decisions.
- [ ] Commit.

### Task 9: Memory stores and curator

**Files:**
- Create: `control-layer/src/memory/memory-types.ts`
- Create: `control-layer/src/memory/memory-store.ts`
- Create: `control-layer/src/memory/curator.ts`
- Test: `control-layer/test/memory/curator.test.ts`

**Interfaces:**
- Memory kinds: `personal`, `project`, `success`, `error`.

- [ ] Test deduplication, merge and stale replacement.
- [ ] Store provenance and project scope.
- [ ] Never persist raw secrets.
- [ ] Add explicit forget/delete path with audit.
- [ ] Commit.

### Task 10: Knowledge ingestion and local retrieval

**Files:**
- Create: `control-layer/src/knowledge/ingest.ts`
- Create: `control-layer/src/knowledge/vector-index.ts`
- Create: `control-layer/src/knowledge/retriever.ts`
- Test: `control-layer/test/knowledge/retriever.test.ts`

**Interfaces:**
- Consumes local files, Markdown-normalized documents and embeddings from `kitz-embed`.
- Produces scoped retrieval with source references.

- [ ] Write tests using deterministic fake embeddings.
- [ ] Chunk text with stable chunk IDs.
- [ ] Store source path/hash and modification time.
- [ ] Re-index only changed chunks.
- [ ] Commit.

### Task 11: Context Intelligence

**Files:**
- Create: `control-layer/src/context/context-builder.ts`
- Test: `control-layer/test/context/context-builder.test.ts`

**Interfaces:**
- Produces minimal task context from project metadata, selected memory, knowledge hits, prompt layers and tool state.

- [ ] Test token-budget prioritization.
- [ ] Prevent cross-project memory leakage.
- [ ] Prefer recent verified success/error memories for matching tasks.
- [ ] Commit.

### Task 12: Verification gate

- [ ] Run all type checks and unit tests.
- [ ] Verify project path escape attacks are blocked.
- [ ] Verify secrets are redacted from logs and audit payloads.
- [ ] Verify agent runs cannot execute ungranted capabilities.
- [ ] Verify memory and retrieval stay project-scoped.
- [ ] Commit any test-only corrections separately.
