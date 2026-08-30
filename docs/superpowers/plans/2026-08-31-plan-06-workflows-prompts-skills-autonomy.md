# Workflows, Prompts, Skills and Autonomous Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement reusable workflows, prompt intelligence, skill lifecycle management and safe autonomous improvement with measurable promotion/rollback.

**Architecture:** Repeated successful execution patterns can become workflow or skill candidates, but candidates remain inactive until tests and qualification pass. Prompts use layered composition and benchmarked version promotion. Improvement never changes immutable safety rules or secret handling.

**Tech Stack:** TypeScript, SQLite, Zod, Vitest, existing event bus/task/agent/model services.

**Spec:** `docs/architecture/master-design.md` and Prompt/Skill/Workflow decisions from Q33 onward.

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Workflow schema and registry

**Files:**
- Create: `control-layer/src/workflows/workflow-types.ts`
- Create: `control-layer/src/workflows/workflow-registry.ts`
- Test: `control-layer/test/workflows/workflow-registry.test.ts`

**Interfaces:**
- Workflow nodes: task, agent, tool, condition, approval, wait, output.
- Produces versioned workflow definitions with project/global scope.

- [ ] Write schema validation tests for valid DAG and cycle rejection.
- [ ] Store workflow version and provenance.
- [ ] Commit.

### Task 2: Workflow execution engine

**Files:**
- Create: `control-layer/src/workflows/workflow-engine.ts`
- Test: `control-layer/test/workflows/workflow-engine.test.ts`

- [ ] Test deterministic two-step workflow.
- [ ] Test conditional branch and Smart Guard approval node.
- [ ] Persist node state so execution resumes after restart.
- [ ] Commit.

### Task 3: Workflow candidate miner

**Files:**
- Create: `control-layer/src/workflows/candidate-miner.ts`
- Test: `control-layer/test/workflows/candidate-miner.test.ts`

- [ ] Test repeated successful action sequences become one deduplicated candidate.
- [ ] Require minimum evidence count and success ratio.
- [ ] Never infer privileged capabilities beyond observed approved execution.
- [ ] Commit.

### Task 4: Layered prompt model

**Files:**
- Create: `control-layer/src/prompts/prompt-types.ts`
- Create: `control-layer/src/prompts/prompt-composer.ts`
- Test: `control-layer/test/prompts/prompt-composer.test.ts`

**Layer order:** Global Base -> Agent Prompt -> Project Prompt -> Skill Prompt -> Task Context.

- [ ] Write tests for deterministic layer order and omission of unused layers.
- [ ] Add token-budget trimming rules that never remove immutable safety layer.
- [ ] Commit.

### Task 5: Prompt registry and versioning

**Files:**
- Create: `control-layer/src/prompts/prompt-store.ts`
- Test: `control-layer/test/prompts/prompt-store.test.ts`

- [ ] Test create version, activate version and rollback.
- [ ] Persist category, agent, model role, project, tools, score, latency and token metadata.
- [ ] Commit.

### Task 6: Prompt benchmark lab

**Files:**
- Create: `control-layer/src/prompts/prompt-benchmark.ts`
- Create: `benchmarks/prompt-suites/core.json`
- Test: `control-layer/test/prompts/prompt-benchmark.test.ts`

- [ ] Test candidate-vs-stable scoring with deterministic fixtures.
- [ ] Require quality non-regression and configured token/latency bounds before promotion.
- [ ] Record benchmark evidence with prompt version.
- [ ] Commit.

### Task 7: Dynamic prompt router

**Files:**
- Create: `control-layer/src/prompts/prompt-router.ts`
- Test: `control-layer/test/prompts/prompt-router.test.ts`

- [ ] Test route selection by agent/task/project/model role.
- [ ] Ensure project prompts cannot override immutable safety constraints.
- [ ] Add safe fallback to stable global/agent prompt.
- [ ] Commit.

### Task 8: Skill schema and registry

**Files:**
- Create: `control-layer/src/skills/skill-types.ts`
- Create: `control-layer/src/skills/skill-store.ts`
- Test: `control-layer/test/skills/skill-store.test.ts`

- [ ] Test metadata for source, revision, capabilities, inputs, outputs, tests and score.
- [ ] Store installed and candidate states separately.
- [ ] Commit.

### Task 9: Skill Scout and qualification

**Files:**
- Create: `control-layer/src/skills/skill-scout.ts`
- Create: `control-layer/src/skills/skill-qualifier.ts`
- Test: `control-layer/test/skills/skill-qualifier.test.ts`

- [ ] Test source inspection with fake GitHub catalog responses.
- [ ] Reject capability mismatch and missing test evidence.
- [ ] Sandbox candidate before activation.
- [ ] Commit.

### Task 10: Autonomous skill factory

**Files:**
- Create: `control-layer/src/skills/skill-factory.ts`
- Test: `control-layer/test/skills/skill-factory.test.ts`

- [ ] Test repeated verified workflow pattern -> generated skill candidate metadata.
- [ ] Generated skills start inactive.
- [ ] Require qualification tests before activation.
- [ ] Version and rollback generated skills.
- [ ] Commit.

### Task 11: Improvement scoreboard

**Files:**
- Create: `control-layer/src/improvement/scoreboard.ts`
- Create: `control-layer/src/improvement/promotion-policy.ts`
- Test: `control-layer/test/improvement/promotion-policy.test.ts`

**Interfaces:**
- Tracks success rate, failure rate, latency, token usage, memory pressure and user override rate for model/prompt/skill/workflow candidates.

- [ ] Test shadow candidate comparison.
- [ ] Test automatic promotion only when thresholds pass.
- [ ] Test automatic rollback on post-promotion regression.
- [ ] Commit.

### Task 12: Improvement activity and audit

**Files:**
- Create: `control-layer/src/improvement/improvement-events.ts`
- Test: `control-layer/test/improvement/improvement-events.test.ts`

- [ ] Emit before/after version, benchmark, reason and rollback pointer.
- [ ] Surface events to activity timeline without exposing prompt secrets or private memory.
- [ ] Commit.

### Task 13: Verification gate

- [ ] Run workflow, prompt, skill and improvement tests.
- [ ] Verify no candidate becomes active without qualification evidence.
- [ ] Verify immutable safety constraints cannot be changed by project/skill prompts.
- [ ] Verify rollback returns exact previous stable versions.
- [ ] Commit test-only corrections separately.
