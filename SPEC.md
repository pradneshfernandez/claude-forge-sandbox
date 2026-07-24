# SPEC — todo-cli (toy CLI todo app)

> Status: dry-run spec produced by /plan for T-004 (pipeline proof). Deliberately tiny.
> Interview answers supplied by the orchestrator on the user's behalf for this
> disposable demo. The one intentionally-open detail — *where the JSON file lives* — was
> answered as a real, documented decision (ADR-002), not a silent assumption.

## Summary
A single-user command-line todo manager that stores tasks in a local JSON file using
only the Python standard library (zero third-party dependencies). Its purpose is to
exercise the Forge pipeline end-to-end (plan → decompose → execute → review → handoff),
not to ship a production tool.

## Users & use cases
- **User:** one local developer tracking personal tasks from a terminal.
- **Use cases:**
  1. Add a todo with free-text description.
  2. List all todos with id, done/undone state, and text.
  3. Mark a todo complete by id.
  4. Delete a todo by id.
- No concurrent users, no network clients, no shared state.

## Functional scope
### In scope
- CLI with four subcommands:
  - `todo add "<text>"` → append a todo; print the new todo's id.
  - `todo list` → print all todos, one per line: `<id> [ ] text` / `<id> [x] text`.
  - `todo done <id>` → set `done=true`; error to stderr + exit 1 if id absent.
  - `todo rm <id>` → delete the todo; error to stderr + exit 1 if id absent.
  - `todo edit <id> "<new text>"` → replace the todo's text; error to stderr + exit 1
    if id absent or new text is empty after `.strip()` (same rule as `add`). Does
    NOT change `done` state. Added post-dry-run (wave 7, T-011) to measure a real
    /execute-wave; see docs/telemetry.md.
- Persistence to a single JSON file (see Data model).
- File + parent dir auto-created on first write if missing.
- Storage path: `~/.todo-cli/todos.json` (ADR-002), overridable via the `TODO_FILE`
  environment variable (used for test isolation).
- Deterministic, human-readable JSON (2-space indent).
- Exit codes: `0` success; `1` user error (bad id, bad/missing args); `2` corrupt store.

### Explicit NON-goals
- No sync, no multi-user, no auth/accounts, no network access.
- No recurring tasks, due dates, reminders, priorities, tags, or search.
- No undo/history; no editing of `done` state via `edit` (use `done`), no edit history.
- No config file (only the `TODO_FILE` env var for path override).
- No TUI / colors / interactive prompts.
- No third-party dependencies; no packaging/PyPI publish; no build step.
- No concurrency/locking guarantees (single local user assumed).

## Architecture
Three-module Python package under `examples/todo-cli/` with a strict dependency
direction (ADR-003):

- `core.py` — pure, I/O-free operations over an in-memory list of todos:
  `add_todo`, `mark_done`, `remove_todo`, `format_list`. Allocates the next id as
  `max(existing ids, default 0) + 1`. No filesystem, no `json`.
- `storage.py` — the only filesystem/`json` module: `resolve_path()`, `load(path)`,
  `save(path, todos)`. Parses the (untrusted) store defensively and writes atomically.
- `todo.py` — argparse CLI: parse argv → `storage.load` → dispatch to `core` →
  `storage.save` → format output + exit code. The only `__main__` entry point.

Data flow: `todo.py` → `storage.load` → `core.*` (returns new/mutated list) →
`storage.save`. `core` never imports `storage`; `storage` never imports `core`.

ADRs: ADR-001 (Python stdlib), ADR-002 (storage format + home-dir location),
ADR-003 (module boundaries & error model).

## Data model
On-disk store is a **JSON array of todo objects** (no wrapper):
```json
[
  { "id": 1, "text": "buy milk",  "done": false },
  { "id": 2, "text": "write spec", "done": true  }
]
```
Types:
- Top level: JSON array. Missing file ⇒ treated as empty array `[]`.
- Each object:
  - `id`: int, unique within the file. Next id = `max(ids, default 0) + 1`; ids of
    deleted todos are not reused within a single process run.
  - `text`: str, non-empty after `.strip()`; stored trimmed. Empty/whitespace ⇒ exit 1.
  - `done`: bool.
- Loader rejects any store whose top level is not a list, or whose items are not objects
  with the exact `{id:int, text:str, done:bool}` shape ⇒ exit 2 (fail closed).

## External services & integrations
None. N/A — fully local, offline, stdlib-only. No API keys, no accounts. The only
environment variable is the optional `TODO_FILE` path override.

## Security requirements
- **Threat model:** local-only tool; no network, no secrets, no auth surface. Per the
  orchestrator's interview answer, security sensitivity is **none**.
- **Defensive requirements (functional, still required):**
  - `storage.load` catches `json.JSONDecodeError` and type-checks the top-level shape,
    failing closed with exit 2 rather than crashing or corrupting data.
  - `storage.save` writes atomically: temp file in the same dir + `os.replace()` so an
    interrupted run cannot truncate an existing store.
  - No `shell=True`, no `eval`, no `pickle`. Path is the resolved `TODO_FILE`/default only.
- **Decomposition flag:** `storage.py` is the one module doing JSON deserialization +
  filesystem writes. Given local-only, no-secrets, no-network scope, `security-review`
  defaults to **false**; the Decomposer may set it `true` for `storage.py` at its
  discretion (cheap, and deserialization is on protocol §6's list). `core.py` and
  `todo.py`: `false`.
- **Data classification:** none / public (user's own local task text).

## Toolchain  ← executors trust this blindly; must be exact
- Language/runtime + version: **Python 3.11** (any 3.11.x; stdlib only).
- Package manager: **none** (zero third-party deps; no pip/venv/lockfile).
- Install: `python3 --version` (no install step; verify interpreter ≥ 3.11).
- Build: N/A (interpreted).
- Test: `python3 -m unittest discover -s examples/todo-cli -p 'test_*.py'`
- Lint: `python3 -m py_compile examples/todo-cli/core.py examples/todo-cli/storage.py examples/todo-cli/todo.py`
- Dev / run: `python3 examples/todo-cli/todo.py <subcommand> [args]`
- Test framework + patterns file: **stdlib `unittest`**; tests in
  `examples/todo-cli/tests/test_*.py`, one file per module. Chosen over pytest to keep
  the "no deps" guarantee (no pip install, no venv, no CI package step). Tests set
  `TODO_FILE` to a temp path for isolation.

## Quality bar
- unittest coverage of: `add`, `list`, `done`, `delete`, and a JSON persistence
  round-trip; plus `storage` failure modes (missing file, empty file, corrupt JSON,
  wrong top-level type, bad id).
- Performance: trivial; store assumed < 10k todos. No perf budget.
- No accessibility / browser / OS matrix (CLI; Linux/macOS shells, Python-portable).
- `verify:` (test + lint commands above) must exit 0 for every code task.

## Deployment target
None. Runs from source via `python3 examples/todo-cli/todo.py`. No install, no container,
no CI deploy. (Framework CI wiring is separate — T-005.)

## Open questions
_None._ The deliberately-open storage-location detail is resolved in ADR-002
(`~/.todo-cli/todos.json`, `TODO_FILE`-overridable). No USER_ACTIONS items are required:
the app is fully local with no accounts, keys, spend, or third-party choices for the
human to make. Ready for /decompose.
