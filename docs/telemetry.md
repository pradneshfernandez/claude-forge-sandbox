# Token telemetry baseline (T-006)

Recorded 2026-07-14, after the todo-cli dry run (waves 1–6). Purpose: future
framework changes get measured against these numbers, not vibed.

## Model versions in use

| Role tier | Model (as pinned in agent files) |
|-----------|----------------------------------|
| Planner / Decomposer / Security-reviewer | opus |
| Implementer-heavy / Test-writer / Code-reviewer | sonnet |
| Implementer / Explorer / Doc-writer | haiku |

Orchestrating sessions for the dry run ran on Opus-class models (pre-split repo);
this baseline session ran on Fable 5 (`claude-fable-5`).

## Baseline — structural cost profile of the dry run

Per-wave token counts were **not persisted** from the original dry-run session
(the `.claude/audit/` JSONL log lived in the pre-split repo and was not carried
over — this is exactly the gap this baseline exists to close going forward).
What is verifiable from the repo itself:

| Metric | Value |
|--------|-------|
| Tasks executed to done | 8 (T-001, T-002, T-004, T-007–T-010) |
| Tasks deferred | 1 (T-003) |
| Waves run | 6 (waves 4–6 = the 4-task todo-cli DAG) |
| Max parallel tasks in a wave | 2 (T-008 + T-009, disjoint owns) |
| BLOCKED escalations | 0 |
| Review rounds beyond first pass | 1 (CHANGES on T-009 storage.py; fixed + reverified) |
| Real bugs caught by review | 1 (atomic-write temp file placed outside target dir) |
| Unit tests produced (by separate test-writer agent) | 47, all passing |
| USER_ACTIONS items raised instead of guessing | 3 (UA-1..UA-3) |
| Invented credentials/URLs/schemas | 0 |

## How to measure (do this every wave from now on)

1. At session start, run `/context` — record the fixed floor (CLAUDE.md + rules
   + tool schemas) before any work.
2. Run exactly one wave in the session (`/execute-wave`), then `/usage` — record
   total tokens for the session; attribute it to that wave.
3. Count tool calls: `wc -l .claude/audit/*.jsonl` before and after the wave;
   the delta is the wave's tool-call volume.
4. Append one row per wave to the table below. Note model, wave number, task IDs.
5. Commit `.claude/audit/` line-count deltas in the row, not the log itself
   (the log is gitignored).

## Per-wave log (append-only)

| Date | Wave | Tasks | Session model | /context floor | /usage total | Tool calls (audit Δ) |
|------|------|-------|---------------|----------------|--------------|-----------------------|
| 2026-07-25 | 7 | T-011 | orchestrator: Sonnet 5; both subagents: sonnet (pinned) | n/a¹ | n/a¹ | n/a¹ |
| _—_  | _next wave: start here_ | | | | | |

¹ The orchestrating session for this wave was launched from outside the sandbox
repo's own Claude Code root, so its `.claude/audit/` hooks never fired and
`/context`/`/usage` (interactive-CLI-only meta-commands) weren't queryable via
tool calls. What IS real, measured data — reported directly by each subagent's
completion event, not estimated — for wave 7 (adding `todo edit`, T-011):

| Subagent | Role | Tokens | Tool calls | Duration |
|----------|------|--------|-----------|----------|
| a1aa618730cb6ba5e | implementer-heavy (T-011: core.py + todo.py) | 30,283 | 8 | 29.8s |
| acb9cb055c4a5f993 | test-writer (test_core.py + test_todo.py) | 32,605 | 5 | 30.6s |
| **Total** | | **62,888** | **13** | **~60s wall (sequential)** |

Outcome: tests 47 → 61 (+14, all passing), verify command exits 0, 0 BLOCKED
escalations, 0 review rounds beyond first pass (test-writer's independent tests
passed against the implementer's first attempt), files touched exactly matched
each task's `owns:`/`tests:` declaration (checked via `git status` equivalent —
diff scoped to core.py, todo.py, test_core.py, test_todo.py, plus the
bookkeeping files SPEC.md/STATE.md/tasks/T-011.md).

To get a true `/context` + `/usage` orchestrator-side number, the next wave
must be run from an interactive `claude` session rooted at
`claude-forge-project-files/claude-forge-sandbox` itself (not from this
parent-directory session) — run `/context` before, `/execute-wave`, then
`/usage` after, per the steps above.
