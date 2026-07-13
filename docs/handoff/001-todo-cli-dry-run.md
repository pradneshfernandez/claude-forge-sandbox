# Handoff 001 — 2026-07-13 — wave 6 complete

## Completed this session
- T-001 Verify policy hooks fire correctly
- T-002 Tailor permission allow-list to the project toolchain
- T-007 Scaffold todo-cli package skeleton & test-package marker
- T-008 Implement core.py pure todo operations (14 unit tests, all pass)
- T-009 Implement storage.py JSON persistence with atomic writes (13 unit tests, 1 CHANGES round fixed, all pass)
- T-010 Implement todo.py argparse CLI wiring core and storage (20 integration tests, all pass)

Full dry-run complete: /plan → /decompose → /execute-wave (3 waves: 4, 5, 6) → /review (T-009 CHANGES + fix + reverify) → /handoff.
Total test suite: 47/47 tests pass (core.py 14, storage.py 13, todo.py 20).

## Blocked / waiting
- T-003 (Wire repository governance) — deferred indefinitely; this repo now has a git remote (pradneshfernandez/claude-forge-sandbox), so UA-2 (CODEOWNERS + branch protection setup) is optional/future work, unblocked does not depend on it.

## Decisions made
- ADR-001: Python 3.11 stdlib-only (argparse, json, os, tempfile, datetime, unittest). No pip/venv/third-party deps.
- ADR-002: JSON array storage at `~/.todo-cli/todos.json` (expanduser), overridable via `TODO_FILE` env var. Atomic writes via tempfile + os.replace(). Closed-form validation on load.
- ADR-003: Three-module architecture (core.py pure logic, storage.py I/O-only, todo.py CLI wiring) with strict one-way dependency: todo.py → storage.py, todo.py → core.py, storage.py ⊥ core.py. Module-level exception CorruptStoreError for storage load failures.

## Files changed
- examples/todo-cli/README.md (created)
- examples/todo-cli/core.py (created)
- examples/todo-cli/storage.py (created)
- examples/todo-cli/todo.py (created)
- examples/todo-cli/tests/__init__.py (created)
- examples/todo-cli/tests/test_core.py (created by test-writer)
- examples/todo-cli/tests/test_storage.py (created by test-writer)
- examples/todo-cli/tests/test_todo.py (created by test-writer)
- SPEC.md (created)
- docs/adr/001-language-python-stdlib.md (created)
- docs/adr/002-json-file-storage.md (created)
- docs/adr/003-module-boundaries.md (created)
- tasks/T-001.md through T-010.md (created by decomposer)
- docs/STATE.md (created)

## Gotchas discovered
1. **docs/STATE.md task-board table drift:** The task-board table in STATE.md is hand-maintained and a duplicate of tasks/*.md frontmatter. It drifted out of sync twice this session (wave numbers, task statuses) and had to be manually reconciled. No automation/script generates it from task file frontmatter. Future improvement: tooling to regenerate the table on-the-fly from tasks/*.md instead of requiring edits in two places.

2. **Ownership boundary not hook-enforced:** The `owns:` field in task frontmatter is treated as convention + orchestrator manual git-status spot-checks during /review. There is no git hook that prevents an implementer subagent from touching a file outside its `owns:` list; enforcement is purely in task instructions ("don't do this") and post-execution audit. Consider adding a pre-commit hook to verify no diff touches unowned paths.

3. **Framework tooling is snapshot, not synced:** This repo (.claude/, framework/) is a point-in-time copy of the sister repo (~/forge). If agents/commands/hooks/templates improve in ~/forge, they must be manually re-copied here; there is no submodule or symlink mechanism. Mark in CLAUDE.md / a README note if framework upgrades are needed.

## Review summary
- **T-008 (core.py):** Code-reviewer approved on first pass. No findings.
- **T-009 (storage.py):** Code-reviewer flagged a bug in wave 5, review round: `tempfile.mkstemp(dir=parent_dir if parent_dir else None)` falls back to system temp when `parent_dir == ""` (e.g., relative `TODO_FILE=todos.json`), placing temp in `/tmp` instead of cwd, violating the "same directory" requirement and risking cross-device `os.replace()` failure. **Fix applied:** changed to `dir=parent_dir or "."` or simply `dir=parent_dir`. Re-verified: all 47 tests pass. Security-reviewer (opus) approved storage.py on first pass (deserialization is strict/fail-closed, path handling has no injection vector, atomic-write pattern sound). Minor non-blocking note: `resolve_path()` uses `.strip()` on `TODO_FILE` (unrequested but harmless).
- **T-010 (todo.py):** Code-reviewer approved on first pass. No findings.

## Open USER_ACTIONS
- UA-1 (Settings allow-list tailoring): Completed; no toolchain yet, so no diff applied.
- UA-2 (CODEOWNERS + branch protection): Deferred. This repo now has a real GitHub remote. Setup is optional; revisit if user wants governance wired in.
- UA-3 (CI workflow proposal for T-005): Will be created when T-005 runs in next wave.

## Next command
`/execute-wave` — runs T-005 (Generate CI toolchain jobs, wave 3, pending) and T-006 (Token telemetry baseline, wave 3, pending). Both depend on T-004, which is now effectively complete.

Precedent: read docs/STATE.md + this file before starting the next wave.
