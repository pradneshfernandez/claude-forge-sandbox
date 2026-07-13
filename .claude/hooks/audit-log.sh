#!/usr/bin/env bash
# Append every tool call to a JSONL audit log. Answers "what did the agent do last Tuesday?"
mkdir -p "$CLAUDE_PROJECT_DIR/.claude/audit"
INPUT=$(cat)
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"event\":$INPUT}" >> "$CLAUDE_PROJECT_DIR/.claude/audit/tool-calls.jsonl"
exit 0
