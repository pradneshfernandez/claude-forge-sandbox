### UA-<n>: <imperative title, e.g. "Create a Stripe account and copy the secret key">
- **Status:** open | done
- **Blocks:** T-###, T-###
- **Required or optional:** required (blocks real work) | optional hardening (skippable, say so plainly — don't bury it in Status prose)
- **What this actually does:** one sentence, mechanism not marketing — no jargon
  the user would need to look up. If it's a no-op under some common condition
  (e.g. solo maintainer, no PR workflow, no team yet), say that condition here,
  not just "why it's needed."
- **Skip if:** the specific condition under which doing this would have zero
  effect right now. Omit this line only for actions with no such condition
  (e.g. genuinely always-needed credentials).
- **Why it's needed (when it applies):** one sentence.
- **Exact steps:**
  1. Go to <exact URL / dashboard path>
  2. <click-by-click steps — assume zero prior knowledge>
  3. Copy the value that looks like `<shape, e.g. sk_live_...>`
- **Where to put it:** add `<ENV_VAR_NAME>=<value>` to `.env` (never commit .env;
  `.env.example` already lists the variable name)
- **Cost/plan implications:** free tier ok? paid? which plan?
- **When done:** change Status to done and tell Claude "UA-<n> done".
