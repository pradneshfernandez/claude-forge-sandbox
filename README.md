# forge-sandbox

Working instance of the [Forge framework](../forge) used to dry-run the pipeline
end-to-end and record token-usage/telemetry baselines. Contains a real task DAG
(tasks/), the toy `todo-cli` demo app it built (examples/todo-cli/), and SPEC.md /
docs/STATE.md for that run.

This repo carries its own copy of .claude/ (needed to actually run
Claude Code commands here) — mirrored from the canonical ../forge repo. If you
change agents/commands/hooks, make the change in ../forge and re-sync here.
