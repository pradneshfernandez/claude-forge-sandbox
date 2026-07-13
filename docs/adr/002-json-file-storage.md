# ADR 002: JSON file storage, home-dir location, atomic writes
- **Status:** accepted
- **Date:** 2026-07-13
## Context
The app must persist todos with no database and no third-party deps, and needs a single
predictable rule for *where* the file lives — the detail deliberately left open in the
toy prompt so it would be decided and documented, not silently assumed. The two candidate
locations were (a) `./todos.json` relative to the current working directory, or (b) a
fixed path in the user's home directory. An interrupted write must not corrupt the store.
## Decision
Store all todos as one **JSON array** (schema in SPEC §Data model), written with 2-space
indent. **Location:** a fixed path in the user's home directory,
`~/.todo-cli/todos.json` (expanded via `os.path.expanduser`); the parent directory is
created on first write. The `TODO_FILE` environment variable overrides this path (used by
tests for isolation). **Atomic writes:** write to a temp file in the same directory, then
`os.replace()` onto the target. The loader validates the top-level shape and fails closed
(exit 2) on corrupt content instead of overwriting it.
## Alternatives considered
- **(a) `./todos.json` (cwd-relative):** rejected — the store would silently change with
  the shell's working directory, surprising the user and scattering todo files.
- **SQLite (`sqlite3` is stdlib):** overkill for a toy; JSON is more inspectable.
- **In-place truncate+write:** rejected — an interrupted run could destroy the store.
## Consequences
Easier: one predictable, greppable, hand-editable store regardless of cwd; trivial
serialization; safe against partial writes.
Harder: no concurrency safety (acceptable — single local user, out of scope); the whole
file is rewritten on every mutation (fine at toy scale, < 10k todos).
Bet: home-dir predictability is worth more than cwd-relative flexibility for this tool.
