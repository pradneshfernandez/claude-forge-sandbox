#!/usr/bin/env bash
# Enforce task `owns:` boundaries mechanically (PROTOCOL.md §4/§6).
#
# While any tasks/T-*.md has `status: in-progress`, Edit/Write calls may only
# touch: the union of those tasks' `owns:` and `tests:` paths, plus the
# pipeline's own bookkeeping files (tasks/, docs/STATE.md, docs/handoff/,
# USER_ACTIONS.md). With no task in-progress (planning, review, handoff
# sessions), the hook is a no-op.
INPUT=$(cat)
python3 - "$CLAUDE_PROJECT_DIR" <<'PYEOF' "$INPUT"
import json, os, re, sys
from pathlib import Path

root = Path(sys.argv[1] or ".").resolve()
data = json.loads(sys.argv[2])
file_path = (data.get("tool_input") or {}).get("file_path", "")
if not file_path:
    sys.exit(0)

try:
    rel = Path(file_path).resolve().relative_to(root).as_posix()
except ValueError:
    rel = Path(file_path).as_posix()  # outside project dir: judge as-is

ALWAYS = ("tasks/", "docs/STATE.md", "docs/handoff/", "USER_ACTIONS.md")
if rel.startswith(ALWAYS[0]) or rel == ALWAYS[1] or rel.startswith(ALWAYS[2]) or rel == ALWAYS[3]:
    sys.exit(0)

def frontmatter(text):
    m = re.match(r"\A---\s*\n(.*?)\n---", text, re.DOTALL)
    return m.group(1) if m else ""

def paths_of(fm, key):
    out = []
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.MULTILINE)
    if not m:
        return out
    inline = m.group(1).strip()
    if inline.startswith("["):
        out += [x.strip().strip("\"'") for x in inline[1:-1].split(",") if x.strip()]
    else:
        block = re.search(rf"^{key}:\s*\n((?:\s+-\s+.*\n?)+)", fm, re.MULTILINE)
        if block:
            out += [l.strip()[1:].strip().strip("\"'")
                    for l in block.group(1).splitlines() if l.strip().startswith("-")]
    return out

active, allowed = [], []
for task in sorted((root / "tasks").glob("T-*.md")):
    fm = frontmatter(task.read_text(encoding="utf-8"))
    if re.search(r"^status:\s*in-progress\s*$", fm, re.MULTILINE):
        active.append(task.stem)
        allowed += paths_of(fm, "owns") + paths_of(fm, "tests")

if not active:
    sys.exit(0)  # no wave running: unrestricted session

for entry in allowed:
    entry = entry.rstrip("/")
    if rel == entry or rel.startswith(entry + "/"):
        sys.exit(0)

reason = (f"{rel} is outside the owns:/tests: paths of the in-progress task(s) "
          f"{', '.join(active)}. A task may only touch files it owns "
          f"(PROTOCOL.md §4). Fix the task's owns: list or hand this file "
          f"to the task that owns it.")
print(json.dumps({"decision": "block", "reason": reason}))
PYEOF
exit 0
