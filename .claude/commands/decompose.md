---
description: Turn the approved SPEC.md into a parallel task DAG in tasks/
---
Preconditions: SPEC.md exists and the user approved it. If not, stop and say so.

Delegate to the **decomposer** subagent (model: opus — pin it): "Read SPEC.md and
.claude/PROTOCOL.md §4. Produce tasks/T-###.md files per TASK_TEMPLATE.md and
write the wave table to docs/STATE.md. Maximize parallelism via disjoint ownership
and interface-first tasks. Default haiku, escalate to sonnet only with a stated
reason in the task file."

When done: present the user a compact wave plan — wave number, task IDs + titles,
model per task, and which tasks are waiting-on-user — and the total open
USER_ACTIONS count. Ask for approval before the first /execute-wave.
