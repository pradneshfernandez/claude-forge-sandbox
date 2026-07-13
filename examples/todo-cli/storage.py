import os
import json
import tempfile


class CorruptStoreError(Exception):
    """Raised when the store file is corrupted or invalid."""
    pass


def resolve_path() -> str:
    """Resolve the storage file path.

    Returns the value of TODO_FILE environment variable if set and non-empty,
    otherwise returns the default path ~/.todo-cli/todos.json
    """
    todo_file = os.environ.get("TODO_FILE", "").strip()
    if todo_file:
        return todo_file
    return os.path.join(os.path.expanduser("~"), ".todo-cli", "todos.json")


def load(path: str) -> list:
    """Load todos from the store file.

    Args:
        path: Path to the JSON store file.

    Returns:
        A list of todo dicts with keys {"id", "text", "done"}.
        Returns an empty list if the file doesn't exist or is empty/whitespace-only.

    Raises:
        CorruptStoreError: If the file contains invalid JSON or doesn't match the schema.
    """
    # Handle non-existent file
    if not os.path.exists(path):
        return []

    # Read the file
    with open(path, 'r') as f:
        content = f.read()

    # Handle empty or whitespace-only file
    if not content.strip():
        return []

    # Parse JSON
    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise CorruptStoreError(f"Invalid JSON: {e}")

    # Validate top level is a list
    if not isinstance(data, list):
        raise CorruptStoreError("Store must be a JSON array at the top level")

    # Validate each item
    for item in data:
        # Must be a dict
        if not isinstance(item, dict):
            raise CorruptStoreError("Each item must be a dict")

        # Must have exactly the keys {"id", "text", "done"}
        if set(item.keys()) != {"id", "text", "done"}:
            raise CorruptStoreError(f"Item has wrong keys: {set(item.keys())}, expected {{'id', 'text', 'done'}}")

        # Validate id: int and not bool
        if not (isinstance(item["id"], int) and not isinstance(item["id"], bool)):
            raise CorruptStoreError(f"id must be int (not bool), got {type(item['id'])}")

        # Validate text: str
        if not isinstance(item["text"], str):
            raise CorruptStoreError(f"text must be str, got {type(item['text'])}")

        # Validate done: bool
        if not isinstance(item["done"], bool):
            raise CorruptStoreError(f"done must be bool, got {type(item['done'])}")

    return data


def save(path: str, todos: list) -> None:
    """Save todos to the store file atomically.

    Args:
        path: Path to the JSON store file.
        todos: List of todo dicts to save.

    Raises:
        OSError: If file operations fail.
    """
    parent_dir = os.path.dirname(path)

    # Ensure parent directory exists (skip if dirname is empty)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)

    # Create temp file in the same directory as the target path
    temp_fd, temp_path = tempfile.mkstemp(dir=parent_dir if parent_dir else None)

    try:
        # Write JSON to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(todos, f, indent=2)
            f.write('\n')  # Add trailing newline

        # Atomically replace the target file
        os.replace(temp_path, path)
    except Exception:
        # Clean up temp file on any exception
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise
