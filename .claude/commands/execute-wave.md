---
description: Run all ready tasks in parallel subagents, then verify
---
1. Read docs/STATE.md and the frontmatter of every file in tasks/. Compute the
   ready set (deps done, no open USER_ACTIONS referenced). If empty because of
   waiting-on-user tasks: list exactly what the user must do (from USER_ACTIONS.md)
   and stop.
2. Assert ownership disjointness across the ready set. On conflict: report, stop.
3. Spawn ALL ready tasks in parallel — one Task call per task in a single turn,
   without waiting between them. Route by frontmatter: model haiku → implementer,
   sonnet → implementer-heavy. ALWAYS pass model explicitly. Give each subagent
   ONLY its task file path and the context files that task references.
4. As implementation tasks return, spawn **test-writer** (sonnet, pinned) for each
   task with a `tests:` field, in parallel where ownership allows.
5. Run each task's `verify:` command. Pass → status: review. Fail → let the same
   implementer retry with the failure output, max 3 attempts, then it must file
   BLOCKED and you set status: blocked.
6. Update docs/STATE.md (statuses, wave counter). Report ≤20 lines: done / review /
   blocked / waiting-on-user, plus any BLOCKED summaries verbatim.
7. If any BLOCKED files exist: recommend the user run /plan to route them to the
   planner before the next wave. Never work around a block yourself.
