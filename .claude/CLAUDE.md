# Forge — plan smart, execute cheap, review hard

This repo runs the Forge orchestration framework. Full protocol: @PROTOCOL.md
(Read .claude/PROTOCOL.md before your first action in any session.)

## Pipeline
1. `/plan` — Opus interviews the user, writes SPEC.md + USER_ACTIONS.md
2. `/decompose` — Opus turns SPEC.md into a task DAG in tasks/
3. `/execute-wave` — all ready tasks run as parallel subagents (cheap models, pinned)
4. `/review` — security + quality review of changed files (strong model)
5. `/handoff` — write docs/handoff/ entry, update docs/STATE.md

## Hard rules (non-negotiable)
- NEVER assume, guess, mock, stub, or invent: credentials, API keys, URLs, schemas,
  business rules, or requirements. Missing info → STOP. Ask the user directly, or add
  an item to USER_ACTIONS.md and mark the task BLOCKED. No silent compromises.
- A task may only touch files listed in its `owns:` field (hook-enforced while a
  wave is in flight).
- The STATE.md task board is generated: `python3 .claude/scripts/forge-state.py
  --write`. Never hand-edit the marker block.
- The implementer of a task NEVER writes or edits its tests. Different agent, always.
- Pin `model:` explicitly on every subagent invocation. Never rely on inheritance.
- Blocked after 3 attempts → write tasks/BLOCKED-<id>.md and stop. Do not improvise.
- Done = acceptance criteria met + tests pass + lint clean + no secrets in diff.
- Prefer editing existing files over creating new ones. No drive-by refactors.

## Context economy
- Use Explore subagents for codebase research; never dump whole directories into context.
- Reference files by exact path + line range in task files.
- One session per wave. `/clear` between unrelated work.

## Toolchain
Defined per-project in SPEC.md §Toolchain (populated by /plan). Do not guess commands.

## When compacting
Always preserve: modified file list, in-flight task IDs, test commands,
open USER_ACTIONS items, and the current wave number.
