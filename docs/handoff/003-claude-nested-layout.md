# Handoff 003 — 2026-07-14 — .claude-nested layout + docs

## Completed this session (framework + instance)

- **Layout refactor (both repos):** the entire framework now nests inside
  `.claude/` (CLAUDE.md, PROTOCOL.md, USAGE.md, settings.json, agents/,
  commands/, hooks/, rules/, templates/, scripts/). Root-level `framework/`,
  FORGE-README.md, SECURITY.md, and empty scaffolding were deleted. Install is
  now "copy the `.claude/` folder", nothing else. Verified against Claude Code
  docs: `.claude/CLAUDE.md` is a supported memory location and the
  `@PROTOCOL.md` import resolves relative to the importing file.
- **`.claudeignore` removed (both repos):** confirmed it is not a Claude Code
  feature — it was inert since day one. Its intent now lives as `Read(...)`
  deny rules in `.claude/settings.json` (node_modules, dist/build/coverage,
  lockfiles, `__pycache__`, minified assets). Settings are byte-identical
  between framework and sandbox.
- **`.claude/USAGE.md` added:** human operating manual (wave loop, blocked-task
  flow, task frontmatter cheat sheet, scripts, cost hygiene). Synced here via
  sync-instance.sh; linked from the framework README.
- `forge-state.py` now bootstraps `docs/STATE.md` (with markers) when the file
  doesn't exist, since the framework no longer ships scaffolding.

## Gotchas discovered

- Sandbox commit `772e444` says "docs: add usage guide" but contains only the
  sync-script half — a wiring command ran in the wrong directory. Content was
  corrected in `4591c1f`; history left as-is (no force-push per policy).
- When running multi-repo sessions from the workspace root, prefer absolute
  paths — relative paths follow the shell's last `cd`.

## Review summary

Verified by execution: 47/47 todo-cli tests, `forge-state.py --check` green,
`bash -n` on all hooks/scripts, settings.json parity diff, USAGE.md present
post-sync. No agent review rounds this session (tooling/docs only).

## Open USER_ACTIONS

- UA-2 (branch protection) — deferred indefinitely, optional.
- Confirm GitHub Actions runs are green on both repos after today's pushes.

## Next command

No ready tasks. Candidates for a next session: `/plan` a new sandbox spec, or
framework work — auto-append the telemetry per-wave row from /execute-wave.
