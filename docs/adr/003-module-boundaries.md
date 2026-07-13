# ADR 003: Module boundaries and error model (core / storage / cli)
- **Status:** accepted
- **Date:** 2026-07-13
## Context
The dry-run must produce a task DAG with at least two tasks that run in parallel on
disjoint `owns:` paths. The code therefore needs a decomposition into independent units
with a clear dependency edge, plus a consistent error/exit-code model across them. All
source lives under `examples/todo-cli/`.
## Decision
Split into three modules with a strict dependency direction:
- `examples/todo-cli/core.py` — pure, I/O-free todo operations over a list
  (parallelizable unit A).
- `examples/todo-cli/storage.py` — the only filesystem/`json` module: resolve path,
  parse/validate, atomic save (parallelizable unit B).
- `examples/todo-cli/todo.py` — argparse CLI wiring `storage` + `core`, owning exit
  codes and output (depends on A and B).
Error model: `core` raises `KeyError`/`ValueError` for bad ids/empty text → CLI maps to
exit 1; `storage` raises a typed `StoreError` on corrupt store → CLI maps to exit 2;
success → exit 0. `core` and `storage` never import each other.
## Alternatives considered
- **Single-file script:** simplest, but yields no parallel-wave DAG — defeats the T-004
  demo goal of proving ≥2 parallel tasks with disjoint ownership.
- **core imports storage:** rejected — couples pure logic to I/O, hurts testability and
  ownership disjointness.
## Consequences
Easier: `core.py` and `storage.py` are implemented and tested in parallel by different
agents on disjoint paths; each unit-tested in isolation.
Harder: three files plus a thin CLI seam instead of one script.
Bet: the extra structure is justified by the pipeline-proof objective.
