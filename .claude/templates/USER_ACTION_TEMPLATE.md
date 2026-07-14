### UA-<n>: <imperative title, e.g. "Create a Stripe account and copy the secret key">
- **Status:** open | done
- **Blocks:** T-###, T-###
- **Why it's needed:** one sentence.
- **Exact steps:**
  1. Go to <exact URL / dashboard path>
  2. <click-by-click steps — assume zero prior knowledge>
  3. Copy the value that looks like `<shape, e.g. sk_live_...>`
- **Where to put it:** add `<ENV_VAR_NAME>=<value>` to `.env` (never commit .env;
  `.env.example` already lists the variable name)
- **Cost/plan implications:** free tier ok? paid? which plan?
- **When done:** change Status to done and tell Claude "UA-<n> done".
