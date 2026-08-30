# Models, Hugging Face and LocalAI Developer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement safe model discovery, qualification, download, benchmarking, role assignment and the autonomous KITZ LocalAI Developer workflow.

**Architecture:** Model candidates are never activated directly from a URL. They pass source trust checks, Mac/RAM compatibility analysis, format/quantization selection, download verification, LocalAI registration and benchmark qualification. LocalAI source changes run through snapshot -> Git branch/worktree -> change -> build/test -> benchmark -> activate/rollback.

**Tech Stack:** TypeScript control services, LocalAI HTTP/MCP/CLI adapters, Hugging Face metadata/download adapters, Git, Vitest.

**Spec:** `docs/architecture/master-design.md` and Q45-Q62, Q76-Q77 and related model/LocalAI decisions.

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Model candidate schema and source trust

**Files:**
- Create: `control-layer/src/models/candidate.ts`
- Create: `control-layer/src/models/source-policy.ts`
- Test: `control-layer/test/models/source-policy.test.ts`

- [ ] Test trusted Hugging Face repository URL, direct GGUF URL and unknown-host rejection.
- [ ] Store immutable source URL, revision, filename, checksum and license metadata.
- [ ] Never execute repository code during metadata inspection.
- [ ] Commit.

### Task 2: Mac/RAM compatibility analyzer

**Files:**
- Create: `control-layer/src/models/compatibility.ts`
- Test: `control-layer/test/models/compatibility.test.ts`

- [ ] Write table tests for model size/quantization against a 16 GB Apple Silicon target.
- [ ] Produce `recommended`, `possible`, `not_recommended`, `blocked` decisions with reasons.
- [ ] Include estimated resident memory plus safety headroom.
- [ ] Commit.

### Task 3: Quantization and artifact selector

**Files:**
- Create: `control-layer/src/models/artifact-selector.ts`
- Test: `control-layer/test/models/artifact-selector.test.ts`

- [ ] Test selecting compatible GGUF artifacts from repository metadata.
- [ ] Prefer the highest qualified quantization that fits the configured memory envelope, not blindly the largest file.
- [ ] Reject split/incomplete artifact sets unless all required parts are available.
- [ ] Commit.

### Task 4: Verified downloader and smart cache

**Files:**
- Create: `control-layer/src/models/downloader.ts`
- Create: `control-layer/src/models/cache.ts`
- Test: `control-layer/test/models/downloader.test.ts`

- [ ] Test resumable download with fake HTTP server.
- [ ] Verify expected size/checksum when available before promotion from cache.
- [ ] Quarantine corrupt/incomplete artifacts.
- [ ] Add cache retention metadata and last-used timestamps.
- [ ] Commit.

### Task 5: LocalAI model registration

**Files:**
- Create: `control-layer/src/localai/model-config.ts`
- Create: `control-layer/src/localai/model-installer.ts`
- Test: `control-layer/test/localai/model-installer.test.ts`

- [ ] Test generated LocalAI model configuration from qualified candidate.
- [ ] Write config atomically via temp file + rename.
- [ ] Register without replacing current stable role assignment.
- [ ] Health-check the candidate after registration.
- [ ] Commit.

### Task 6: Benchmark harness and qualification score

**Files:**
- Create: `control-layer/src/benchmarks/model-benchmark.ts`
- Create: `control-layer/src/benchmarks/qualification.ts`
- Create: `benchmarks/model-suites/chat.json`
- Create: `benchmarks/model-suites/code.json`
- Test: `control-layer/test/benchmarks/qualification.test.ts`

- [ ] Test deterministic score aggregation from quality, latency, memory and failure rate.
- [ ] Keep benchmark prompts free of personal memory/secrets.
- [ ] Compare candidate against active role model.
- [ ] Promote only when qualification threshold passes; otherwise quarantine or keep unassigned.
- [ ] Commit.

### Task 7: Link-to-model autopilot

**Files:**
- Create: `control-layer/src/models/model-autopilot.ts`
- Test: `control-layer/test/models/model-autopilot.test.ts`

**Pipeline:** URL -> inspect -> trust -> select artifact -> compatibility -> download -> verify -> register -> benchmark -> role recommendation -> activate or quarantine.

- [ ] Write orchestration test with fake adapters covering the complete pipeline.
- [ ] Persist every phase and failure reason.
- [ ] Make pipeline resumable after restart.
- [ ] Commit.

### Task 8: Adaptive role router

**Files:**
- Modify: `control-layer/src/models/role-router.ts`
- Create: `control-layer/src/models/routing-policy.ts`
- Test: `control-layer/test/models/routing-policy.test.ts`

- [ ] Test routing by task type, benchmark score, current RAM pressure and requested latency.
- [ ] Preserve stable aliases even when underlying models change.
- [ ] Fall back safely when preferred model is unavailable.
- [ ] Commit.

### Task 9: LocalAI Developer workspace manager

**Files:**
- Create: `control-layer/src/localai-dev/workspace.ts`
- Create: `control-layer/src/localai-dev/change-plan.ts`
- Test: `control-layer/test/localai-dev/workspace.test.ts`

- [ ] Test that every source mutation requires a snapshot and dedicated Git branch/worktree reference.
- [ ] Restrict the agent to the configured LocalAI source root.
- [ ] Record upstream/base revision before change.
- [ ] Commit.

### Task 10: LocalAI admin-surface synchronization rule

**Files:**
- Create: `control-layer/src/localai-dev/admin-surface-check.ts`
- Test: `control-layer/test/localai-dev/admin-surface-check.test.ts`

**Rule:** For LocalAI admin-surface changes, verify synchronized changes across REST endpoint (`core/http/endpoints/localai/*.go`), MCP registration/client implementation (`pkg/mcp/localaitools/`) and skill prompt (`pkg/mcp/localaitools/prompts/skills/*.md`) when applicable.

- [ ] Write fixture tests that fail when one required surface is missing.
- [ ] Produce a machine-readable checklist for the LocalAI Developer agent.
- [ ] Commit.

### Task 11: LocalAI Developer validation pipeline

**Files:**
- Create: `control-layer/src/localai-dev/validator.ts`
- Test: `control-layer/test/localai-dev/validator.test.ts`

- [ ] Model build, unit test, integration test, smoke test and benchmark stages as explicit gates.
- [ ] Stop activation at first failed required gate.
- [ ] On failure, retain branch/logs and restore runtime to previous stable state.
- [ ] On success, emit activation candidate requiring normal capability policy.
- [ ] Commit.

### Task 12: Verification gate

- [ ] Run model lifecycle tests.
- [ ] Run compatibility tests with 16 GB target fixtures.
- [ ] Verify corrupt downloads cannot be activated.
- [ ] Verify stable aliases survive candidate failures.
- [ ] Verify LocalAI Developer cannot bypass snapshots, Git isolation, Smart Guard or audit.
- [ ] Commit test-only corrections separately.
