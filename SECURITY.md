# Security Policy

## Framework security model
Defense in depth around an AI agent with real execution authority:
1. **Permissions as code** — .claude/settings.json (committed) denies secret reads,
   raw network fetches (curl/wget), destructive commands, force-push, publish, sudo.
   Everything with side effects is ask-gated.
2. **Deterministic hooks** — every tool call audited to .claude/audit/tool-calls.jsonl;
   edits to .claude/, .github/workflows/, .mcp.json, CODEOWNERS blocked;
   credential-shaped strings in commands blocked.
3. **Untrusted input doctrine** — file contents, web pages, and tool output are data,
   not instructions. Agents confirm with the user before acting on embedded instructions.
4. **No secrets in context** — secrets live in .env (gitignored) / a secrets manager,
   referenced by env var name only. .env.example documents names, never values.
5. **Review gates** — security-sensitive diffs require opus security review mapped to
   OWASP Top 10; CI runs secret scanning, SAST, and dependency audit on every PR.
6. **Human-owned surfaces** — CI workflows, hooks, settings, CODEOWNERS are edited by
   humans only (hook-enforced + CODEOWNERS-enforced).

## Operational rules
- Never run `--dangerously-skip-permissions` outside an isolated container/VM.
- Start Claude Code from the repo root, never from $HOME.
- Keep Claude Code updated; review .claude/audit/ periodically.
- Rotate immediately any secret that ever appears in a conversation or log.

## Reporting a vulnerability
Open a private security advisory on the repository (GitHub → Security → Advisories).
