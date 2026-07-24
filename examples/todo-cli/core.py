"""Pure, I/O-free todo operations over an in-memory list."""


def add_todo(todos: list, text: str) -> tuple:
    """Add a todo to the list.

    Args:
        todos: List of todo dicts.
        text: Todo text (will be stripped).

    Returns:
        Tuple of (updated todos list, new_id).

    Raises:
        ValueError: If text is empty after stripping.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("Text cannot be empty")

    new_id = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": new_id, "text": stripped, "done": False})
    return (todos, new_id)


def mark_done(todos: list, todo_id: int) -> list:
    """Mark a todo as done.

    Args:
        todos: List of todo dicts.
        todo_id: ID of the todo to mark done.

    Returns:
        The updated todos list.

    Raises:
        KeyError: If todo_id is not found.
    """
    for todo in todos:
        if todo["id"] == todo_id:
            todo["done"] = True
            return todos
    raise KeyError(todo_id)


def edit_todo(todos: list, todo_id: int, text: str) -> list:
    """Edit a todo's text.

    Args:
        todos: List of todo dicts.
        todo_id: ID of the todo to edit.
        text: New todo text (will be stripped).

    Returns:
        The updated todos list.

    Raises:
        KeyError: If todo_id is not found.
        ValueError: If text is empty after stripping.
    """
    for todo in todos:
        if todo["id"] == todo_id:
            stripped = text.strip()
            if not stripped:
                raise ValueError("Text cannot be empty")
            todo["text"] = stripped
            return todos
    raise KeyError(todo_id)


def remove_todo(todos: list, todo_id: int) -> list:
    """Remove a todo from the list.

    Args:
        todos: List of todo dicts.
        todo_id: ID of the todo to remove.

    Returns:
        The updated todos list.

    Raises:
        KeyError: If todo_id is not found.
    """
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return todos
    raise KeyError(todo_id)


def format_list(todos: list) -> str:
    """Format todos as a human-readable string.

    Args:
        todos: List of todo dicts.

    Returns:
        String with one line per todo, or empty string if list is empty.
        Format: "id [ ] text" for uncompleted, "id [x] text" for completed.
    """
    if not todos:
        return ""

    lines = []
    for todo in todos:
        status = "[x]" if todo["done"] else "[ ]"
        lines.append(f"{todo['id']} {status} {todo['text']}")

    return "\n".join(lines)
