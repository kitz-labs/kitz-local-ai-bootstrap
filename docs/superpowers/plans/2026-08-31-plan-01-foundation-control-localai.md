# Foundation, Control Layer and LocalAI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Establish the repository foundation, shared configuration, Control Layer core, event bus, LocalAI client, model registry and health endpoints.

**Architecture:** A TypeScript Control Layer owns state and orchestration. LocalAI is accessed through a dedicated adapter. Shared contracts are isolated from UI and infrastructure. Runtime data lives outside Git-tracked source paths under the configured KITZLABS root.

**Tech Stack:** Node.js, TypeScript, Fastify, Zod, SQLite, Vitest.

**Spec:** `docs/architecture/master-design.md`

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Create application workspace and shared contracts

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `tsconfig.base.json`
- Create: `control-layer/package.json`
- Create: `control-layer/tsconfig.json`
- Create: `control-layer/src/contracts/system.ts`
- Test: `control-layer/test/contracts/system.test.ts`

**Interfaces:**
- Produces: `SystemHealth`, `ModelRole`, `ProjectId`, `AgentId`, `TaskId` types.

- [ ] **Step 1: Write failing contract validation test**

```ts
import { describe, expect, it } from 'vitest';
import { ModelRoleSchema } from '../../src/contracts/system';

describe('ModelRoleSchema', () => {
  it('accepts only stable KITZ model roles', () => {
    expect(ModelRoleSchema.parse('kitz-main')).toBe('kitz-main');
    expect(() => ModelRoleSchema.parse('random')).toThrow();
  });
});
```

- [ ] **Step 2: Run test**

Run: `pnpm --filter control-layer test -- system.test.ts`
Expected: FAIL because contracts do not exist.

- [ ] **Step 3: Implement contracts**

Define Zod schemas for `kitz-main`, `kitz-code`, `kitz-fast`, `kitz-embed` and branded string identifiers.

- [ ] **Step 4: Run tests**

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add package.json pnpm-workspace.yaml tsconfig.base.json control-layer
git commit -m "feat: establish control layer workspace and contracts"
```

### Task 2: Implement runtime path configuration

**Files:**
- Create: `control-layer/src/config/runtime-paths.ts`
- Create: `control-layer/src/config/env.ts`
- Test: `control-layer/test/config/runtime-paths.test.ts`

**Interfaces:**
- Produces: `getRuntimePaths(homeDir?: string)` returning paths for `apps`, `models`, `agents`, `skills`, `memory`, `knowledge`, `projects`, `config`, `logs`, `backups`, `cache`.

- [ ] Write a failing test asserting default root `~/KITZLABS-AI` and deterministic subpaths.
- [ ] Run the test and confirm failure.
- [ ] Implement path resolution without creating directories as a side effect.
- [ ] Add `KITZLABS_ROOT` override validation.
- [ ] Run tests and commit with `feat: add managed KITZLABS runtime paths`.

### Task 3: Add SQLite state database

**Files:**
- Create: `control-layer/src/db/client.ts`
- Create: `control-layer/src/db/migrations/001_core.sql`
- Create: `control-layer/src/db/migrate.ts`
- Test: `control-layer/test/db/migrations.test.ts`

**Interfaces:**
- Produces tables: `projects`, `tasks`, `agents`, `models`, `events`, `audit_log`, `settings`.

- [ ] Write a failing in-memory migration test.
- [ ] Create migration with foreign keys and ISO timestamps.
- [ ] Ensure migrations are idempotent.
- [ ] Verify schema with `PRAGMA foreign_key_check`.
- [ ] Commit.

### Task 4: Implement event bus

**Files:**
- Create: `control-layer/src/events/event-types.ts`
- Create: `control-layer/src/events/event-bus.ts`
- Test: `control-layer/test/events/event-bus.test.ts`

**Interfaces:**
- Produces: `publish(event)`, `subscribe(type, handler)`, `unsubscribe()`.
- Event categories: `system`, `project`, `task`, `agent`, `model`, `tool`, `security`, `recovery`.

- [ ] Write tests for ordered local delivery and handler isolation.
- [ ] Implement an in-process typed event bus.
- [ ] Persist selected events asynchronously to `events` table.
- [ ] Verify a failing subscriber does not break other subscribers.
- [ ] Commit.

### Task 5: Build Control Layer HTTP server

**Files:**
- Create: `control-layer/src/server/app.ts`
- Create: `control-layer/src/server/routes/health.ts`
- Create: `control-layer/src/index.ts`
- Test: `control-layer/test/server/health.test.ts`

**Interfaces:**
- Produces: `GET /health`, `GET /api/system/status`.

- [ ] Write failing Fastify injection tests.
- [ ] Implement server factory with no listen side effect.
- [ ] Return structured health containing service state and timestamp.
- [ ] Start listener only from `src/index.ts`.
- [ ] Commit.

### Task 6: Implement LocalAI client adapter

**Files:**
- Create: `control-layer/src/localai/client.ts`
- Create: `control-layer/src/localai/types.ts`
- Test: `control-layer/test/localai/client.test.ts`

**Interfaces:**
- Produces: `LocalAIClient.health()`, `listModels()`, `chat()`, `embeddings()`.

- [ ] Write tests using a mocked HTTP server.
- [ ] Validate response payloads with Zod.
- [ ] Apply short timeouts and explicit error classes (`LocalAIUnavailableError`, `LocalAIProtocolError`).
- [ ] Ensure secrets or full prompt content are not logged.
- [ ] Commit.

### Task 7: Implement model registry and stable role aliases

**Files:**
- Create: `control-layer/src/models/registry.ts`
- Create: `control-layer/src/models/role-router.ts`
- Create: `control-layer/src/models/model-store.ts`
- Test: `control-layer/test/models/registry.test.ts`

**Interfaces:**
- Produces: `registerModel()`, `assignRole()`, `resolveRole()`, `quarantineModel()`.

- [ ] Write tests proving each stable role resolves to one active model or an explicit unavailable state.
- [ ] Persist registry records in SQLite.
- [ ] Prevent quarantined models from resolving.
- [ ] Record role changes in audit log.
- [ ] Commit.

### Task 8: Add Mac capability detector

**Files:**
- Create: `control-layer/src/system/mac-capabilities.ts`
- Test: `control-layer/test/system/mac-capabilities.test.ts`

**Interfaces:**
- Produces: normalized `{ arch, totalMemoryBytes, appleSilicon, metalExpected }`.

- [ ] Write parser tests using injected command outputs.
- [ ] Never shell from pure parser functions.
- [ ] Add a thin runtime collector around `uname` and `sysctl`.
- [ ] Surface warnings if architecture is unsupported or memory is below target.
- [ ] Commit.

### Task 9: Add LocalAI health aggregation

**Files:**
- Create: `control-layer/src/system/health-service.ts`
- Modify: `control-layer/src/server/routes/health.ts`
- Test: `control-layer/test/system/health-service.test.ts`

**Interfaces:**
- Consumes: LocalAI client, database, model registry, Mac capability detector.
- Produces: `SystemHealth` summary used later by Cockpit Live Bar.

- [ ] Write tests for healthy, degraded and unavailable LocalAI states.
- [ ] Implement aggregation without turning one degraded dependency into a server crash.
- [ ] Return actionable German status text plus machine-readable codes.
- [ ] Commit.

### Task 10: Verification gate

- [ ] Run `pnpm -r typecheck`.
- [ ] Run `pnpm -r test`.
- [ ] Start Control Layer locally and verify `/health`.
- [ ] Verify LocalAI-down state is reported as degraded, not fatal.
- [ ] Verify no runtime data is written into Git-tracked folders except test fixtures.
- [ ] Commit any test-only fixes separately.
