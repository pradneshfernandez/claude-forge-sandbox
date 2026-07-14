# Forge usage guide

For the human driving the sessions. (PROTOCOL.md is the spec the agents follow;
this file is how *you* operate the pipeline day to day.)

## Starting a project

```
claude                          # at your project root
/plan build a <thing that does X>
```

Opus interviews you — answer precisely, it will not guess what you don't say.
It writes `SPEC.md` (what's being built, toolchain, architecture) and
`USER_ACTIONS.md` (things only you can do). **Read SPEC.md before approving.**
Everything downstream treats it as ground truth.

Then:

```
/decompose
```

This produces the task DAG in `tasks/T-###.md`. Skim the frontmatter: does the
wave order make sense, are the `owns:` paths right, is anything suspiciously big?
Cheaper to fix the plan now than mid-wave.

## The wave loop

One wave per session — this is the core discipline:

```
/execute-wave     # runs all ready tasks as parallel pinned subagents
/review           # code review + security review of what changed
/handoff          # writes docs/handoff/NNN.md, regenerates docs/STATE.md
```

Then start a fresh session (or `/clear`) for the next wave. Repeat until
`/status` shows no ready tasks.

## Resuming after a break

New session, then:

> Read docs/STATE.md and the latest docs/handoff entry, then continue.

`/status` any time for the board. Never re-explain the project from memory —
if STATE.md and the handoff don't carry enough to resume, that's a bug in the
handoff, fix it there.

## Your side of the contract

- **USER_ACTIONS.md** is your checklist. Agents park anything only you can do
  there (API keys, accounts, DNS, spend approval) and keep working on what's
  unblocked. When you finish one, say: `UA-3 done`.
- **Protected paths** (`.claude/`, `.github/workflows/`) are hook-blocked for
  agents. When a task needs a change there, it hands you a diff — you review
  and paste it yourself. That friction is the security model, not a bug.
- **Questions over guesses.** If Claude asks instead of assuming, that's the
  framework working. Answer, don't say "just pick something".

## When a task blocks

After 3 failed attempts (or genuine ambiguity) a task writes
`tasks/BLOCKED-T-###.md` and stops. Read it, then either fix the cause
(usually an under-specified task file — re-run `/decompose` on that slice) or
answer the open question and re-run the wave. A Haiku task that keeps failing
needs a better task file, not a bigger model.

## Task file cheat sheet

```yaml
id: T-012            status: pending | ready | in-progress |
wave: 3              #        waiting-on-user | blocked | review | done
depends_on: [T-010]  # all must be done before this runs
owns: [src/api.py]   # ONLY files it may touch (hook-enforced)
model: haiku         # haiku default; sonnet for cross-file reasoning
tests: [tests/test_api.py]   # written by test-writer, never the implementer
security-review: true        # forces opus security review
verify: "pytest -q"          # must exit 0 for done
```

## Scripts

```bash
python3 .claude/scripts/forge-state.py            # print the task board
python3 .claude/scripts/forge-state.py --write    # regenerate docs/STATE.md
python3 .claude/scripts/forge-state.py --check    # CI drift gate (exit 2 on drift)
.claude/scripts/sync-instance.sh /path/to/project # pull tooling updates in
```

The STATE.md board between the `forge:task-board` markers is generated — never
hand-edit it; edit `tasks/*.md` frontmatter and rerun `--write`.

## Cost hygiene

- Record `/context` at session start and `/usage` after each wave in
  `docs/telemetry.md` (one row per wave — the table is already set up).
- Long sessions rot: if a session drifts past one wave of work, hand off and
  restart rather than pushing through.
