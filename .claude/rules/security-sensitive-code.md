---
paths:
  - "**/auth/**"
  - "**/crypto/**"
  - "**/*password*"
  - "**/*token*"
  - "**/*session*"
  - "**/middleware/**"
---
You are touching security-sensitive code. Additional rules:
- Never log tokens, passwords, or PII. Redact in error messages.
- Use the platform's vetted crypto/auth libraries; never hand-roll crypto,
  session logic, or JWT parsing.
- Constant-time comparison for secrets. Parameterized queries only.
- Any new endpoint: explicit authn AND authz check, input validated at the boundary
  with an allowlist schema, rate limiting considered.
- This diff requires security-reviewer approval regardless of task frontmatter.
