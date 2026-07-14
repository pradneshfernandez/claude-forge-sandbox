#!/usr/bin/env bash
# Sync Forge tooling from this framework repo into an instance repo.
#
#   .claude/scripts/sync-instance.sh /path/to/instance-repo
#
# Copies the reusable tooling (agents, commands, hooks, rules, templates,
# scripts, PROTOCOL.md, .claudeignore) and deletes tooling files the framework
# has removed. Never touches instance-owned state: SPEC.md, tasks/, docs/,
# USER_ACTIONS.md, .claude/CLAUDE.md, or .claude/settings.json (both are
# tailored per-project; a settings diff is printed instead if it differs).
set -euo pipefail

SRC="$(cd "$(dirname "$0")/../.." && pwd)"  # .claude/scripts -> repo root
DEST="${1:?usage: sync-instance.sh <instance-repo-root>}"

[ -d "$DEST" ] || { echo "error: $DEST is not a directory" >&2; exit 1; }
[ -d "$DEST/.git" ] || echo "warning: $DEST is not a git repo root — continuing" >&2
[ "$(cd "$DEST" && pwd)" = "$SRC" ] && { echo "error: destination is the framework repo itself" >&2; exit 1; }

SYNC_DIRS=".claude/agents .claude/commands .claude/hooks .claude/rules .claude/templates .claude/scripts"
SYNC_FILES=".claude/PROTOCOL.md .claudeignore"

for d in $SYNC_DIRS; do
  mkdir -p "$DEST/$d"
  rsync -a --delete --exclude='__pycache__' --itemize-changes "$SRC/$d/" "$DEST/$d/" | sed "s|^|  $d/: |"
done
for f in $SYNC_FILES; do
  rsync -a --itemize-changes "$SRC/$f" "$DEST/$f" | sed "s|^|  $f: |"
done

if ! diff -q "$SRC/.claude/settings.json" "$DEST/.claude/settings.json" >/dev/null 2>&1; then
  echo ""
  echo "NOTE: .claude/settings.json differs and was NOT synced (per-project policy)."
  echo "Review manually:  diff $SRC/.claude/settings.json $DEST/.claude/settings.json"
fi

echo ""
echo "Synced Forge tooling: $SRC -> $DEST"
