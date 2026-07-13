# Project State

- **Phase:** bootstrap — wave 1 complete (T-003 deferred, not blocking); todo-cli fully built, tested, and reviewed (T-007–T-010 all done). Next: /execute-wave for T-005/T-006.
- **Current wave:** 6 complete; reviewed (1 CHANGES round on T-009, fixed and reverified)
- **Last handoff:** docs/handoff/001-todo-cli-dry-run.md

## Task board
| ID | Title | Status | Wave | Model | Owns (top path) |
|----|-------|--------|------|-------|-----------------|
| T-001 | Verify policy hooks fire correctly | done | 1 | haiku | .claude/audit/ |
| T-002 | Tailor permission allow-list | done | 1 | haiku | — (propose only) |
| T-003 | Wire repository governance | deferred | 1 | haiku | — (guide only) |
| T-004 | Pipeline dry run on toy spec | done | 2 | sonnet | SPEC.md, tasks/ |
| T-005 | Generate CI toolchain jobs | pending | 3 | haiku | — (propose only) |
| T-006 | Token telemetry baseline | pending | 3 | haiku | docs/telemetry.md |
| T-007 | Scaffold todo-cli package skeleton & test-package marker | done | 4 | haiku | examples/todo-cli/tests/__init__.py |
| T-008 | Implement core.py pure todo operations | done | 5 | haiku | examples/todo-cli/core.py |
| T-009 | Implement storage.py JSON persistence (atomic) | done | 5 | haiku | examples/todo-cli/storage.py |
| T-010 | Implement todo.py argparse CLI | done | 6 | sonnet | examples/todo-cli/todo.py |

## Waves (todo-cli, from T-004 decomposition)
| Wave | Tasks (parallel) | Depends on | Notes |
|------|------------------|------------|-------|
| 4 | T-007 | — | Interface-first: package dir + tests/__init__.py so unittest discovery works |
| 5 | T-008, T-009 | T-007 | Disjoint owns (core.py vs storage.py); no import between them; run in parallel |
| 6 | T-010 | T-008, T-009 | Integration CLI wiring both modules |

Test files are written by the test-writer (not the implementer), per each task's `tests:` field:
T-008 → tests/test_core.py, T-009 → tests/test_storage.py, T-010 → tests/test_todo.py.

## Blocked
_None._

## Waiting on user
T-003 (UA-2) — deferred indefinitely until this repo has a git remote to protect.
