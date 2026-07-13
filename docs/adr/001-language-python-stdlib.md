# ADR 001: Language = Python 3.11, standard library only
- **Status:** accepted
- **Date:** 2026-07-13
## Context
The toy app must have zero third-party runtime dependencies and be trivial to run and
test from a fresh checkout. It is a dry-run to exercise the Forge pipeline, so the stack
should minimize install/CI friction rather than optimize for anything else. The two
obvious candidates were Python (stdlib `argparse`/`json`) and Node.js (built-in
`node:util parseArgs` / `fs`).
## Decision
Use **Python 3.11**, standard library only. CLI via `argparse`, persistence via `json`,
timestamps via `datetime`, tests via stdlib `unittest`. No pip, no venv, no lockfile.
## Alternatives considered
- **Node.js (stdlib):** viable and dependency-free, but `unittest`-equivalent (`node:test`)
  and arg parsing are less ergonomic for a first-run demo, and Python is more universally
  preinstalled on the target dev/Linux environment.
- **Rust/Go:** introduce a build/toolchain step, contradicting the "trivial to run" goal.
- **Bash:** JSON handling without `jq` (a dependency) is error-prone.
## Consequences
Easier: instant run (`python3 todo.py ...`), no install/build, zero-dep CI.
Harder: no static typing enforcement beyond `py_compile`; linting is minimal (stdlib
`py_compile` only, since ruff/flake8 would be a dependency and need a UA + install).
Bet: for a toy, stdlib-only is worth losing richer lint/type tooling.
