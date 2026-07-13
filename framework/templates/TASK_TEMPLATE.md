---
id: T-000
title: Short imperative title
status: pending          # pending | ready | in-progress | waiting-on-user | blocked | review | done
wave: 0                  # set by decomposer; informational
depends_on: []           # e.g. [T-001, T-002]
owns:                    # ONLY paths this task may create/modify
  - src/example/file.ts
model: haiku             # haiku | sonnet (sonnet requires a reason below)
security-review: false   # true if auth/crypto/input/uploads/payments/SQL/shell/deser
tests: tests/example/file.test.ts   # path(s) the test-writer will own; omit if none
user-actions: []         # USER_ACTIONS item IDs this task depends on, e.g. [UA-3]
verify: "npm run test -- tests/example && npm run lint"
---

## Objective
One paragraph. What exists when this task is done that didn't before.

## Context (read these, nothing else)
- SPEC.md §<section>
- src/reference/similar.ts (lines 10–80) — imitate this pattern
- docs/adr/003-database-choice.md

## Instructions
1. Exact step. Exact path. Exact signature:
   `export async function refreshSession(token: string): Promise<Session>`
2. Next exact step.
3. Handle these specific error cases: <list>.

## Acceptance criteria (each must be mechanically checkable)
- [ ] `refreshSession` returns a new Session for a valid unexpired token
- [ ] Expired token → throws `TokenExpiredError`, does NOT touch the DB
- [ ] All criteria covered by tests in `tests:` path

## Non-goals — do NOT
- Do NOT modify src/auth/login.ts
- Do NOT add any dependency
- Do NOT change the Session type (owned by T-004)

## Model reason (required if model != haiku)
—
