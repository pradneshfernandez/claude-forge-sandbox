---
description: Code review + security review of the current wave, then mark tasks done
---
1. Collect tasks with status: review from docs/STATE.md.
2. Spawn **code-reviewer** (sonnet, pinned) on the wave diff (`git diff` scoped to
   the wave's owned paths) with each task's acceptance criteria.
3. In parallel, spawn **security-reviewer** (opus, pinned) for every task with
   `security-review: true` — and for any diff touching auth, input handling,
   secrets, CI, or infrastructure even if unmarked.
4. APPROVE from all required reviewers → status: done, commit with a conventional
   commit message referencing the task ID (e.g. "feat(auth): T-014 session refresh").
5. CHANGES/BLOCK → status: blocked with the reviewer's findings appended to the
   task file under ## Review findings. These go back through /execute-wave.
6. Update STATE.md. Report verdicts per task in one line each.
