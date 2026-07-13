# Handoff 002 — 2026-07-14 — wave 3 complete + tooling sync

## Completed this session

- **T-005 (CI toolchain jobs):** `test-and-lint` in `.github/workflows/ci.yml` now
  runs the real toolchain: byte-compile lint, the 47-test todo-cli suite
  (`python3 -m unittest discover -s tests -t .` from `examples/todo-cli/`), and a
  STATE.md drift check. Per ADR-001 the toolchain is stdlib-only, so the job uses
  the runner's system python3 — no new actions, nothing new to SHA-pin.
- **T-006 (telemetry baseline):** `docs/telemetry.md` records the dry run's
  structural cost profile plus a ≤15-line measurement procedure and an append-only
  per-wave log table.
- **Tooling sync from claude-forge** (new upstream features, pulled in via the new
  `framework/scripts/sync-instance.sh`):
  - `framework/scripts/forge-state.py` — STATE.md task board is now generated from
    `tasks/*.md` frontmatter between `<!-- forge:task-board:begin/end -->` markers;
    `--check` runs in CI. This closes the "STATE.md drifts" gotcha from handoff 001
    — and the first generated board immediately exposed real drift (truncated
    titles, wrong owns column for T-007) in the old hand-maintained table.
  - `.claude/hooks/enforce-owns.sh` — `owns:` boundaries are now hook-enforced:
    while any task is `in-progress`, Edit/Write outside the union of in-progress
    tasks' `owns:`/`tests:` paths is blocked (bookkeeping files exempt). Closes the
    "owns is convention-only" gotcha. Wired into `.claude/settings.json`.
  - Sync deliberately skips `.claude/settings.json` (per-project policy); the hook
    registration was applied here manually with user approval.

## Blocked / waiting

Nothing blocked. No pending tasks — the DAG is fully executed (T-003 deferred).

## Decisions made

- T-005 was executed as a direct apply, not the propose-and-paste flow: the user
  directed this orchestrating session (running outside the sandbox's hook
  perimeter) to implement and push concrete results, which is the human approval
  the protect-paths policy exists to obtain. UA-3 is marked done with this note.
- No setup-python action: system python3 on ubuntu-latest satisfies the stdlib-only
  toolchain and avoids adding a new supply-chain pin.

## Files changed

- `.github/workflows/ci.yml` — real test-and-lint job (T-005)
- `docs/telemetry.md` — new (T-006)
- `docs/STATE.md` — restructured around generated marker block
- `tasks/T-005.md`, `tasks/T-006.md` — status → done
- `USER_ACTIONS.md` — UA-3 → done
- Synced from upstream: `.claude/hooks/enforce-owns.sh`, `framework/scripts/`,
  `framework/PROTOCOL.md` (§4/§5/§9 updates + new §11 Tooling), `.claude/settings.json`

## Gotchas discovered

- `sync-instance.sh` initially copied `__pycache__/` from framework/scripts;
  fixed upstream with an rsync exclude (claude-forge commit "fix: exclude
  __pycache__ from instance sync").
- The dry run's `.claude/audit/` JSONL didn't survive the repo split, so the
  telemetry baseline has structural counts but no token numbers. The per-wave log
  in telemetry.md exists so this never happens again.

## Review summary

Tooling changes were verified by execution rather than agent review: enforce-owns
hook tested against five cases (owned file allowed, tests path allowed, foreign
file blocked, bookkeeping allowed, no-wave no-op), forge-state.py `--write`/
`--check` round-trip green, full test suite 47/47, CI steps run locally before
commit.

## Open USER_ACTIONS

- UA-2 (branch protection) — deferred indefinitely, optional.
- UA-3 follow-up — confirm the GitHub Actions run is green after this push.

## Next command

No ready tasks. Either `/plan` a new spec for the sandbox, or continue framework
work in claude-forge (candidate: auto-append the telemetry per-wave row from
/execute-wave).
