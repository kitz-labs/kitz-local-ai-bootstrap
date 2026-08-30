# AGENTS.md — KITZLABS AI Codex Operating Rules

These rules apply to Codex and coding agents working in this repository.

## Mission

Implement KITZLABS AI exactly according to the approved architecture while minimizing unnecessary token/context use.

**Priority order:** correctness > safety > tests > maintainability > token efficiency > speed.

Token saving must never mean skipping required validation, security gates, snapshots, reviews, or acceptance tests.

## Canonical sources

Use this order of authority:

1. `docs/architecture/master-design.md`
2. the relevant Q decision in `docs/architecture/questions-*.md`
3. `docs/superpowers/plans/2026-08-31-kitzlabs-ai-master-implementation-plan.md`
4. the currently active subsystem plan
5. existing implementation and tests

Do **not** read all Q001-Q326 on every task. Search for the exact decision ID or topic only when the master design/current plan does not contain enough detail.

## Lean context protocol

For every task:

1. Read this `AGENTS.md` once.
2. Read the master plan once per execution session.
3. Read only the **current subsystem plan**.
4. Extract/use only the **current task brief**.
5. Search the repository before opening files broadly.
6. Read only files and line ranges relevant to the task.
7. Do not paste whole plans, logs, diffs, or prior-task summaries into prompts when a file path can be passed instead.
8. Store durable progress in the Superpowers ledger; do not rely on conversation history.
9. Never re-dispatch a task already marked complete in the ledger.
10. After task completion, report only: status, files changed, tests, commit, concerns.

## Superpowers execution mode

Preferred execution method: **subagent-driven development**.

- isolated worktree/branch
- one focused implementer context per judgment-heavy task
- batch small same-shape mechanical edits when safe
- task-specific review after implementation
- one whole-branch review at the end
- fix loop only for real review findings
- no duplicate worker-spawned reviewers
- no implementation directly on `main`

Use file-based artifacts for task briefs, reports, review packages, and progress ledgers.

## Model/cost routing

Choose the least expensive model that can complete the task reliably.

- **Cheap/fast:** exact mechanical edits, one-file changes, generated boilerplate with complete specification.
- **Standard:** multi-file implementation, integration, debugging, nontrivial tests.
- **Most capable:** architecture conflicts, security-sensitive reasoning, difficult debugging, final whole-branch review.
- **Escalate:** fix-loop rounds 4–5 or repeated failure.

Always specify the subagent model explicitly where the environment supports it. Do not silently inherit an unnecessarily expensive default model.

When the local KITZ model worker is available, low-risk mechanical analysis/summarization may be delegated locally. Codex remains responsible for integration, security-sensitive decisions, and final verification.

## Repository reading rules

Prefer targeted discovery:

- search exact symbol/path/error first
- inspect directory metadata before recursively reading content
- use focused line ranges for large files
- do not reread unchanged files without a reason
- do not scan generated folders, model files, caches, dependencies, build output, or logs unless directly required

Never load model binaries, large generated artifacts, personal memory, or secrets into context.

## Output discipline

During execution, be concise.

Normal progress response format:

```text
Task N: DONE
Changed: <paths>
Tests: <command> — PASS
Commit: <sha>
Concerns: none
```

Do not repeat architecture explanations or previous task summaries unless a new conflict requires them.

## Test strategy

Do not save tokens by removing tests.

Use the smallest valid test scope first:

1. targeted unit/integration test for changed behavior
2. affected package/module suite
3. broader phase suite at subsystem boundaries
4. full acceptance suite before final completion/merge

Do not rerun the entire suite after every tiny edit when targeted tests prove the task and no cross-system boundary changed.

## Git discipline

- work on feature branches/worktrees
- small independently testable commits
- one task or coherent batch per commit
- never force-push shared branches unless explicitly authorized
- prepare PRs with concise summaries and test evidence
- risky changes require snapshot/Git restore point before activation

## Safety invariants

Never bypass:

- Smart Guard
- Secret Vault / Keychain boundary
- audit logging
- project capability policy
- recovery/snapshot requirements
- LocalAI REST/MCP/skill-prompt synchronization rules

Never commit secrets, personal memory raw data, model binaries, `.env` contents, tokens, or private credentials.

## LocalAI rule

For LocalAI source/admin changes, keep these surfaces synchronized when applicable:

1. REST endpoint
2. MCP tool/client implementation
3. LocalAI skill prompt
4. tests

Model/config writes must be atomic where supported. Build/test/benchmark before activation; rollback when validation regresses.

## Hugging Face / model research

Do not repeatedly query or re-evaluate the same model metadata during one task. Cache the qualification result in project artifacts.

For the current 16 GB Apple Silicon target, coding/general model selection must be benchmark-driven. Repository popularity alone is not activation evidence.

## Stop conditions

Stop only for:

- irreversible/destructive operations requiring approval
- security-sensitive external side effects
- merge/publish to shared production targets requiring approval
- a plan/spec conflict where every reasonable path would be a guess

Otherwise make the smallest reversible ruling, record it in the ledger, and continue.

## Definition of efficient

Efficient means:

- no repeated full-context reads
- no repeated historical summaries
- no unnecessary powerful-model usage
- no duplicate reviews
- no redundant full-suite runs
- no broad repo scans when targeted search works

But every completed task still has tests, review evidence, an auditable commit, and a recovery path where required.
