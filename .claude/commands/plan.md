---
description: Interview the user and produce SPEC.md + USER_ACTIONS.md for a new project or feature
---
Read framework/PROTOCOL.md §1–3 if not already in context. Then delegate to the
**planner** subagent (model: opus — pin it) with this brief:

"The user wants to build: $ARGUMENTS

Interview them using AskUserQuestion until the spec is defensible. Cover: users &
use cases, functional scope + explicit NON-goals, stack preference (ask, don't
assume), data model, auth, external services, hosting/budget, testing expectations,
security sensitivity. Apply the No-Assumption Rule: every unknown becomes a question
now or a USER_ACTIONS.md item with step-by-step instructions (where to sign up,
which key to copy, what env var name to put it in — the user should need zero
research). Then write SPEC.md, USER_ACTIONS.md, and ADRs for major choices."

When the planner returns: show the user SPEC.md §Summary and every open
USER_ACTIONS item. Ask for explicit approval before /decompose. Do not start
decomposition without approval.
