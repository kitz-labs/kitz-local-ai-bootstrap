# Connectors, Python App Operator and Cockpit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add guarded external connectors, autonomous web research, GitHub intelligence, Python app control and the full-screen KITZLABS cockpit.

**Architecture:** Connectors implement a common capability-aware adapter contract. Connector calls cannot bypass Tool Gateway/Smart Guard. The Cockpit consumes only Control Layer APIs and event streams.

**Tech Stack:** TypeScript, Fastify, WebSocket/SSE, GitHub API, Playwright-compatible browser adapter, MCP client adapter, Telegram Bot API adapter, React/Next.js for Cockpit, Vitest and Playwright tests.

**Spec:** `docs/architecture/master-design.md`

## Global Constraints

Use all constraints from the master implementation plan.

---

### Task 1: Tool Gateway contract

**Files:**
- Create: `control-layer/src/tools/tool-contract.ts`
- Create: `control-layer/src/tools/tool-gateway.ts`
- Test: `control-layer/test/tools/tool-gateway.test.ts`

**Interfaces:**
- Produces: `executeTool(toolId, input, executionContext)`.
- Execution context includes project, agent, task, requested capability and audit correlation ID.

- [ ] Write failing tests proving every mutation invokes Smart Guard.
- [ ] Add timeout, cancellation and normalized result/error envelopes.
- [ ] Record start/end/error audit events.
- [ ] Commit.

### Task 2: GitHub connector and intelligence service

**Files:**
- Create: `control-layer/src/connectors/github/github-client.ts`
- Create: `control-layer/src/connectors/github/github-service.ts`
- Test: `control-layer/test/connectors/github-service.test.ts`

**Interfaces:**
- Produces read operations for repo/status/branches/commits/issues/PRs/actions and guarded writes for branches/commits/issues/PRs.

- [ ] Write fake-client tests for repository inspection and PR creation.
- [ ] Ensure merge and production-impacting writes map to confirm/deny policies unless explicitly pre-granted.
- [ ] Add CI failure summarization as pure logic with fixture tests.
- [ ] Commit.

### Task 3: Browser and research connectors

**Files:**
- Create: `control-layer/src/connectors/browser/browser-adapter.ts`
- Create: `control-layer/src/connectors/research/research-service.ts`
- Test: `control-layer/test/connectors/research-service.test.ts`

**Interfaces:**
- Browser capabilities: navigate, extract text, structured extract, screenshot metadata, click/fill when granted.
- Research produces sourced notes and optional knowledge-ingestion payloads.

- [ ] Test source deduplication and provenance.
- [ ] Separate deterministic browser automation from crawl/extraction workers.
- [ ] Add project-level allowed-domain policy hooks.
- [ ] Commit.

### Task 4: MCP and API Connector Center

**Files:**
- Create: `control-layer/src/connectors/mcp/mcp-registry.ts`
- Create: `control-layer/src/connectors/api/api-registry.ts`
- Create: `control-layer/src/connectors/connector-service.ts`
- Test: `control-layer/test/connectors/connector-service.test.ts`

**Interfaces:**
- Produces connector registration, health check, enable/disable, capability listing and project binding.

- [ ] Test invalid connector schemas are rejected.
- [ ] Store secrets only as Secret Vault references.
- [ ] Add health states `healthy`, `degraded`, `offline`, `disabled`.
- [ ] Commit.

### Task 5: Telegram Gateway

**Files:**
- Create: `control-layer/src/connectors/telegram/telegram-service.ts`
- Test: `control-layer/test/connectors/telegram-service.test.ts`

**Interfaces:**
- Produces send-message and inbound-event normalization; later workflows consume normalized Telegram events.

- [ ] Test token references are resolved at execution time only.
- [ ] Test inbound updates do not execute privileged actions without policy evaluation.
- [ ] Add project/bot mapping.
- [ ] Commit.

### Task 6: Python App discovery

**Files:**
- Create: `control-layer/src/python-apps/discovery.ts`
- Create: `control-layer/src/python-apps/types.ts`
- Test: `control-layer/test/python-apps/discovery.test.ts`

**Interfaces:**
- Detects `pyproject.toml`, `requirements.txt`, `uv.lock`, entry scripts and likely start commands inside explicitly granted roots.

- [ ] Test detection fixtures.
- [ ] Never execute discovered commands during discovery.
- [ ] Mark uncertain start commands as unverified.
- [ ] Commit.

### Task 7: Python App runtime operator

**Files:**
- Create: `control-layer/src/python-apps/runtime.ts`
- Create: `control-layer/src/python-apps/process-registry.ts`
- Test: `control-layer/test/python-apps/runtime.test.ts`

**Interfaces:**
- Produces start/stop/restart/status/log-tail operations.
- Uses isolated app environment strategy with `uv` where available.

- [ ] Write process lifecycle tests with a harmless fixture app.
- [ ] Prevent working directory escape.
- [ ] Persist only verified successful start commands.
- [ ] Add failure events for root-cause engine.
- [ ] Commit.

### Task 8: Cockpit application shell

**Files:**
- Create: `cockpit/package.json`
- Create: `cockpit/app/layout.tsx`
- Create: `cockpit/app/page.tsx`
- Create: `cockpit/components/navigation/Sidebar.tsx`
- Create: `cockpit/components/live/LiveBar.tsx`
- Create: `cockpit/components/project/ProjectHeader.tsx`
- Test: `cockpit/test/app-shell.test.tsx`

**Interfaces:**
- Produces full-screen layout with fixed smart left sidebar, sticky project header, scrollable center and adaptive right Live Bar.

- [ ] Write component tests for expanded/compact sidebar and Live Bar modes.
- [ ] Implement German labels from architecture.
- [ ] Ensure no narrow centered content wrapper is introduced.
- [ ] Commit.

### Task 9: Cockpit API client and live events

**Files:**
- Create: `cockpit/lib/control-client.ts`
- Create: `cockpit/lib/event-stream.ts`
- Create: `control-layer/src/server/routes/events.ts`
- Test: `cockpit/test/event-stream.test.ts`

**Interfaces:**
- Consumes Control Layer APIs and event stream.
- Produces reconnecting live state for health, agents, tasks and activity.

- [ ] Test reconnect/backoff behavior.
- [ ] Do not expose secrets in serialized events.
- [ ] Commit.

### Task 10: Implement project overview dashboard

**Files:**
- Create: `cockpit/app/projects/[projectId]/page.tsx`
- Create: `cockpit/components/dashboard/MetricStrip.tsx`
- Create: `cockpit/components/dashboard/WorkPanel.tsx`
- Create: `cockpit/components/dashboard/WarningPanel.tsx`
- Create: `cockpit/components/dashboard/ActivityPanel.tsx`
- Create: `cockpit/components/dashboard/TimeMachinePanel.tsx`
- Test: `cockpit/test/project-dashboard.test.tsx`

- [ ] Write tests for Health/Tasks/Agents/Errors/GitHub/Models metrics.
- [ ] Add active work, warnings, tasks/files/GitHub, Hugging Face/models, activities and time machine sections.
- [ ] Keep cards movable/resizable behind a layout manager abstraction.
- [ ] Commit.

### Task 11: Implement primary project pages

**Files:**
- Create routes under `cockpit/app/projects/[projectId]/`: `tasks`, `chats`, `files`, `knowledge`, `memory`, `agents`, `github`, `python-apps`, `workflows`, `schedules`, `prompts`, `skills`, `connectors`, `models`, `activities`, `settings`.
- Create focused components under `cockpit/components/project-pages/`.
- Test: `cockpit/e2e/project-navigation.spec.ts`

- [ ] Add route/navigation E2E test first.
- [ ] Implement task Kanban/list/calendar shells backed by real APIs.
- [ ] Implement three-pane file manager with preview/editor action hooks.
- [ ] Implement agent cards with live status/model/tools/autonomy.
- [ ] Implement GitHub and connector health views.
- [ ] Commit in page-group-sized commits, not one giant commit.

### Task 12: New Chat intelligent start

**Files:**
- Create: `cockpit/app/chat/new/page.tsx`
- Create: `cockpit/components/chat/ChatComposer.tsx`
- Create: `cockpit/components/chat/ExecutionTimeline.tsx`
- Create: `control-layer/src/chat/chat-service.ts`
- Test: `cockpit/e2e/new-chat.spec.ts`

**Interfaces:**
- Auto-detects project, agent, model role, memory/tools and risk mode; manual override remains available.

- [ ] Write E2E test for opening chat and receiving a streamed local response.
- [ ] Add drag/drop metadata pipeline for files/folders/links without leaking ungranted paths.
- [ ] Show Smart Guard approval cards when needed.
- [ ] Show final completion report.
- [ ] Commit.

### Task 13: Verification gate

- [ ] Run Control Layer tests.
- [ ] Run Cockpit unit tests.
- [ ] Run Playwright E2E navigation tests.
- [ ] Verify connector mutations pass Tool Gateway.
- [ ] Verify Python fixture start/stop/restart.
- [ ] Verify full-screen layout at desktop and reduced window sizes.
- [ ] Commit any fixes separately.
