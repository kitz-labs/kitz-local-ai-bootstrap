# Lean Codex Execution Protocol

## Goal

Keep implementation quality maximal while reducing unnecessary context, repeated reading, duplicate reviews, redundant test runs, and expensive model usage.

This protocol complements `AGENTS.md`; it does not replace the architecture or implementation plans.

## Core rule

**Load only what the current task needs. Persist state in files. Reuse evidence. Escalate model capability only when task complexity demands it.**

## Context layers

### Layer 1 — always small

Read once at session start:

- `AGENTS.md`
- `docs/superpowers/plans/2026-08-31-kitzlabs-ai-master-implementation-plan.md`
- the active subsystem plan

### Layer 2 — task only

For the current task:

- task brief
- directly consumed interfaces
- exact files/symbols to modify
- relevant tests
- relevant ledger rulings

### Layer 3 — only on demand

Read only when required to resolve ambiguity/conflict:

- `docs/architecture/master-design.md`
- exact Q decision(s)
- adjacent subsystem plans
- broad git history
- upstream LocalAI/Hugging Face documentation

Never load all Q001-Q326 into every implementation context.

## Search-before-read policy

Before opening many files:

1. identify exact symbol, route, model alias, config key, test name, or error
2. search repository
3. inspect matching paths
4. open the smallest useful line range
5. expand only when evidence requires it

Avoid recursive reading of directories, dependencies, build output, caches, generated artifacts, model files, or large logs.

## Subagent token policy

Use fresh, minimal context per task.

An implementer receives:

- one-line project/task placement
- task brief path
- exact interfaces from prior tasks
- one or two rulings if needed
- report path

It does **not** receive:

- whole conversation history
- all previous task reports
- all architecture documents
- whole plan copied into prompt
- duplicate reviewer instructions

Reviewers receive file paths to:

- task brief
- implementer report
- diff/review package
- concise global constraints

Never paste a full diff when a review-package file is available.

## Model routing

| Task | Model tier |
|---|---|
| exact one-file/mechanical change | cheap/fast |
| boilerplate from complete spec | cheap/fast |
| multi-file integration | standard |
| debugging with uncertain cause | standard |
| security/policy/recovery logic | capable |
| architecture conflict | most capable |
| final branch review | most capable |
| fix rounds 4–5 | one tier above failed implementer |

Using a cheaper model that needs multiple retries is not efficient. Prefer the lowest tier expected to finish correctly in one pass.

## Local model offload

Once LocalAI worker routing is available, optional low-risk helper work can be moved to local models:

- symbol classification
- log condensation
- documentation summarization
- test-output summarization
- simple code explanation
- mechanical refactors with deterministic tests

Current model candidates already tracked in the project include:

- `Qwen3-Coder-30B-A3B-Instruct-GGUF` for coding-oriented local work
- `Qwen3.5-9B` for general/multimodal work

Activation remains benchmark-driven on the actual 16 GB Apple Silicon Mac. Hugging Face popularity/download counts are discovery signals, not qualification evidence.

Codex/high-capability review remains mandatory for security-sensitive integration and final verification.

## Test-cost policy

Test progressively:

1. changed function/unit
2. affected module/package
3. integration boundary if touched
4. phase suite at subsystem completion
5. full acceptance suite at final completion

Do not run the full suite after every mechanical edit. Do not skip targeted tests.

Reuse prior successful evidence only when the tested code/dependency surface has not changed.

## Batch policy

Batch only independent same-shape mechanical edits, for example:

- adding the same field to multiple schemas
- renaming the same constant across known paths
- identical documentation link updates

Do not batch tasks with independent design decisions, different risk profiles, or separate integration boundaries.

## Progress persistence

Use the Superpowers ledger as durable execution memory.

Minimum entries:

- plan identity
- task complete lines with commit range
- fix rounds
- rulings
- deferred minor findings
- blockers

After context compaction or restart, resume from ledger + git history. Never reconstruct progress from conversation memory.

## Output budget

Routine Codex output should be compact:

```text
Task 4: DONE
Changed: control-layer/src/...; tests/...
Tests: pnpm vitest ... — PASS (12/12)
Commit: abc1234
Concerns: none
```

Only expand when:

- a blocker exists
- a security decision was made
- a ruling changes the plan
- tests fail
- final phase/branch summary is required

## Documentation policy

Do not rewrite large architecture documents after every task.

Update documentation only when:

- behavior/contracts changed
- a Q decision was changed
- a new user-visible capability exists
- installer/configuration instructions changed
- a ruling creates a lasting architectural constraint

## Hugging Face query policy

For model research:

1. search once for candidates
2. store candidate metadata/qualification locally
3. inspect README/docs only for shortlisted models
4. download only after compatibility gate
5. benchmark only viable quantizations
6. record result and do not repeat unless model/config/hardware changes

This avoids repeated web/plugin context and unnecessary downloads.

## Quality gates that are never optional

- spec compliance
- targeted tests
- task review
- final whole-branch review
- Smart Guard/security invariants
- secret protection
- recovery path for risky changes
- benchmark/qualification before activating models/prompts/skills/backends

## Expected effect

Most token savings should come from:

1. not loading Q001-Q326 repeatedly
2. not pasting full plans into subagents
3. not repeating prior-task history
4. targeted file search/line reads
5. file-based diff/review packages
6. explicit model-tier routing
7. targeted tests before full suites
8. batching small same-shape work
9. ledger-based resume after compaction
10. local helper models after LocalAI routing is available
