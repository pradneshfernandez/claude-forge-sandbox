import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import storage  # noqa: E402


class ResolvePathTest(unittest.TestCase):
    def setUp(self):
        self._had_env = "TODO_FILE" in os.environ
        self._old_env = os.environ.get("TODO_FILE")

    def tearDown(self):
        if self._had_env:
            os.environ["TODO_FILE"] = self._old_env
        else:
            os.environ.pop("TODO_FILE", None)

    def test_returns_todo_file_env_when_set(self):
        os.environ["TODO_FILE"] = "/custom/path/todos.json"
        self.assertEqual(storage.resolve_path(), "/custom/path/todos.json")

    def test_returns_default_when_unset(self):
        os.environ.pop("TODO_FILE", None)
        expected = os.path.join(os.path.expanduser("~"), ".todo-cli", "todos.json")
        self.assertEqual(storage.resolve_path(), expected)

    def test_returns_default_when_empty(self):
        os.environ["TODO_FILE"] = ""
        expected = os.path.join(os.path.expanduser("~"), ".todo-cli", "todos.json")
        self.assertEqual(storage.resolve_path(), expected)


class LoadTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self._had_env = "TODO_FILE" in os.environ
        self._old_env = os.environ.get("TODO_FILE")

    def tearDown(self):
        if self._had_env:
            os.environ["TODO_FILE"] = self._old_env
        else:
            os.environ.pop("TODO_FILE", None)
        self.tmpdir.cleanup()

    def path(self, name="todos.json"):
        return os.path.join(self.tmpdir.name, name)

    def write(self, name, content):
        p = self.path(name)
        with open(p, "w") as f:
            f.write(content)
        return p

    def test_nonexistent_path_returns_empty_list(self):
        p = self.path("does_not_exist.json")
        self.assertEqual(storage.load(p), [])

    def test_empty_file_returns_empty_list(self):
        p = self.write("empty.json", "")
        self.assertEqual(storage.load(p), [])

    def test_whitespace_only_file_returns_empty_list(self):
        p = self.write("ws.json", "   \n\t  \n")
        self.assertEqual(storage.load(p), [])

    def test_invalid_json_raises_corrupt(self):
        p = self.write("bad.json", "{not valid json")
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_top_level_object_raises_corrupt(self):
        p = self.write("obj.json", json.dumps({"id": 1, "text": "a", "done": False}))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_item_missing_key_raises_corrupt(self):
        p = self.write("missing.json", json.dumps([{"id": 1, "text": "a"}]))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_item_extra_key_raises_corrupt(self):
        p = self.write(
            "extra.json",
            json.dumps([{"id": 1, "text": "a", "done": False, "extra": "x"}]),
        )
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_id_as_bool_raises_corrupt(self):
        p = self.write("idbool.json", json.dumps([{"id": True, "text": "a", "done": False}]))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_id_as_str_raises_corrupt(self):
        p = self.write("idstr.json", json.dumps([{"id": "1", "text": "a", "done": False}]))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_text_as_int_raises_corrupt(self):
        p = self.write("textint.json", json.dumps([{"id": 1, "text": 5, "done": False}]))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_done_as_string_raises_corrupt(self):
        p = self.write("donestr.json", json.dumps([{"id": 1, "text": "a", "done": "false"}]))
        with self.assertRaises(storage.CorruptStoreError):
            storage.load(p)

    def test_valid_single_item_returns_list_of_dicts(self):
        p = self.write("valid.json", json.dumps([{"id": 1, "text": "a", "done": False}]))
        result = storage.load(p)
        self.assertEqual(result, [{"id": 1, "text": "a", "done": False}])
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)


class SaveTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_save_then_load_round_trips(self):
        todos = [
            {"id": 1, "text": "buy milk", "done": False},
            {"id": 2, "text": "walk dog", "done": True},
        ]
        p = os.path.join(self.tmpdir.name, "todos.json")
        storage.save(p, todos)
        self.assertEqual(storage.load(p), todos)

    def test_save_creates_nested_parent_dir(self):
        p = os.path.join(self.tmpdir.name, "nested", "subdir", "todos.json")
        self.assertFalse(os.path.exists(os.path.dirname(p)))
        todos = [{"id": 1, "text": "x", "done": False}]
        storage.save(p, todos)
        self.assertTrue(os.path.exists(p))
        self.assertEqual(storage.load(p), todos)

    def test_saved_file_is_two_space_indented_json(self):
        p = os.path.join(self.tmpdir.name, "todos.json")
        todos = [{"id": 1, "text": "a", "done": False}]
        storage.save(p, todos)
        with open(p, "r") as f:
            raw = f.read()
        # Top-level list items indent 2 spaces; nested dict keys indent 4 spaces.
        self.assertIn('\n  {', raw)
        self.assertIn('\n    "id"', raw)
        self.assertEqual(raw, json.dumps(todos, indent=2) + "\n")


if __name__ == "__main__":
    unittest.main()
