# todo-cli

A stdlib-only single-user CLI todo manager storing tasks in `~/.todo-cli/todos.json`, overridable via `TODO_FILE`.

## Run

```
python3 examples/todo-cli/todo.py <subcommand> [args]
```

## Test

```
python3 -m unittest discover -s examples/todo-cli -p 'test_*.py'
```

## Lint

```
python3 -m py_compile examples/todo-cli/core.py examples/todo-cli/storage.py examples/todo-cli/todo.py
```
