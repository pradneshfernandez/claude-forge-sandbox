---
description: Write the session handoff and update STATE.md — run before ending any session
---
Delegate to **doc-writer** (haiku, pinned): "Write docs/handoff/NNN-<slug>.md from
.claude/templates/HANDOFF_TEMPLATE.md. NNN = next number in docs/handoff/.
Include: wave number, tasks completed/blocked this session, key decisions (link
ADRs), files changed (from git log since last handoff), gotchas discovered, open
USER_ACTIONS, and the exact next command to run. Update docs/STATE.md last-session
pointer."

Then tell the user: handoff written, next session should start with
"Read docs/STATE.md and the latest docs/handoff entry, then continue" — nothing else
needs to be re-explained.
