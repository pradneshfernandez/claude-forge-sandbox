#!/usr/bin/env bash
# Block bash commands that contain credential-shaped strings (keys pasted into commands).
INPUT=$(cat)
CMD=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)
if echo "$CMD" | grep -qE '(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|xox[baprs]-[A-Za-z0-9-]{10,}|-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY)'; then
  echo '{"decision":"block","reason":"Command contains a credential-like string. Secrets must flow through environment variables, never through commands or chat."}'
  exit 0
fi
exit 0
