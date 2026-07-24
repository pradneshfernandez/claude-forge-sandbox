# User Actions

Things only the human can do. Agents append items here (template:
.claude/templates/USER_ACTION_TEMPLATE.md) instead of guessing, mocking, or
stubbing. When you finish one, mark it done and tell Claude "UA-<n> done".

### UA-1: Apply the tailored permissions diff to .claude/settings.json
- **Status:** done (confirmed no changes needed; generic defaults kept)
- **Blocks:** T-002
- **Why it's needed:** Agents are hook-blocked from editing permission policy; only you can.
- **Note:** This repo has no package.json/pyproject.toml/Cargo.toml of its own — Forge
  is a generic meta-framework meant to be copied into other projects, so there is no
  real toolchain to tailor here yet. No diff is proposed at this time. Confirming this
  is enough to unblock T-002; real tailoring happens per-project after /plan runs there.
- **Exact steps:**
  1. Nothing to apply right now. Tell Claude "UA-1 done" to accept the generic
     npm-shaped defaults as a harmless placeholder.
- **Where to put it:** .claude/settings.json (committed to the repo)
- **Cost/plan implications:** none
- **When done:** tell Claude "UA-1 done".

### UA-2: Set CODEOWNERS and branch protection on GitHub
- **Status:** skipped (2026-07-25, user decision) — see reasoning below.
- **Blocks:** T-003 (T-003 itself blocks nothing else — T-004 does not depend on it)
- **Required or optional:** optional hardening, not required.
- **What this actually does:** CODEOWNERS maps file paths to GitHub usernames so
  GitHub auto-requests them as PR reviewers; paired with a branch-protection
  checkbox, it can also block merging until that reviewer approves. It does
  nothing else — it doesn't restrict who can push directly to a branch.
- **Skip if:** you're the sole committer and push directly to `main` (no PR
  workflow). Both repos here match that today, so CODEOWNERS would be a
  live-nobody file and branch protection's PR-review gate would never trigger.
- **Why it's needed (when it applies):** once there are other contributors or
  you switch to a PR-based workflow, this is how you'd enforce human review of
  agent-written changes before merge.
- **Exact steps (when applicable):**
  1. Create .github/CODEOWNERS with your handle as owner of .claude/ and
     .github/.
  2. GitHub → repo → Settings → Branches → Add branch protection rule for `main`.
  3. Enable: Require a pull request before merging; Require review from Code Owners;
     Require status checks (select: test-and-lint).
- **Where to put it:** GitHub repository settings
- **Cost/plan implications:** free on public repos; private repos need a paid plan for some rules
- **When done:** revisit if/when this project gets a second contributor or moves to a PR workflow.

### UA-3: Paste the generated CI toolchain job into ci.yml
- **Status:** done (2026-07-14) — the user directed the orchestrating session to apply
  the toolchain job directly, so the paste step was not needed. The job uses the
  runner's system python3 (stdlib-only toolchain per ADR-001), so no new action SHAs
  were introduced; checkout remains the only pinned action. Remaining check: confirm
  the Actions run is green on GitHub after the next push.
- **Blocks:** T-005
- **Why it's needed:** Workflow files are a protected path (supply-chain surface).
- **Exact steps:**
  1. Ask Claude for the T-005 workflow diff.
  2. Verify every `uses:` is pinned to a 40-char commit SHA.
  3. Paste into .github/workflows/ci.yml, commit, open a test PR, confirm green.
- **Where to put it:** .github/workflows/ci.yml
- **Cost/plan implications:** GitHub Actions free tier is typically sufficient
- **When done:** tell Claude "UA-3 done".
