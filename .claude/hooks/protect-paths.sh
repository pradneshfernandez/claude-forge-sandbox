#!/usr/bin/env bash
# Block agent edits to security-critical paths. Humans edit these; agents ask.
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)
case "$FILE" in
  *".claude/settings"*|*".claude/hooks"*|*".github/workflows"*|*".mcp.json"*|*"CODEOWNERS"*)
    echo "{\"decision\":\"block\",\"reason\":\"$FILE is a protected policy path. Ask the user to make this change manually, or get explicit approval.\"}"
    exit 0 ;;
esac
exit 0
