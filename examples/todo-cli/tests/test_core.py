"""Unit tests for examples/todo-cli/core.py.

Tests the public contract described in tasks/T-008.md (acceptance criteria),
not the implementation's internals.
"""

import unittest

import core


class AddTodoTests(unittest.TestCase):
    def test_add_to_empty_list(self):
        todos, new_id = core.add_todo([], "buy milk")
        self.assertEqual(
            todos, [{"id": 1, "text": "buy milk", "done": False}]
        )
        self.assertEqual(new_id, 1)

    def test_add_assigns_max_plus_one_not_count_plus_one(self):
        existing = [
            {"id": 1, "text": "a", "done": False},
            {"id": 3, "text": "b", "done": False},
        ]
        todos, new_id = core.add_todo(existing, "c")
        self.assertEqual(new_id, 4)
        self.assertIn({"id": 4, "text": "c", "done": False}, todos)

    def test_add_whitespace_only_raises_value_error(self):
        with self.assertRaises(ValueError):
            core.add_todo([], "   ")

    def test_add_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            core.add_todo([], "")

    def test_add_strips_leading_and_trailing_whitespace(self):
        todos, new_id = core.add_todo([], "  buy milk  ")
        self.assertEqual(todos[0]["text"], "buy milk")

    def test_add_returns_same_list_object_mutated(self):
        todos = []
        result, _ = core.add_todo(todos, "x")
        self.assertIs(result, todos)


class MarkDoneTests(unittest.TestCase):
    def test_missing_id_raises_key_error(self):
        todos = [{"id": 1, "text": "a", "done": False}]
        with self.assertRaises(KeyError):
            core.mark_done(todos, 99)

    def test_present_id_sets_done_true(self):
        todos = [
            {"id": 1, "text": "a", "done": False},
            {"id": 2, "text": "b", "done": False},
        ]
        result = core.mark_done(todos, 2)
        self.assertTrue(result[1]["done"])
        self.assertFalse(result[0]["done"])

    def test_mark_done_on_empty_list_raises_key_error(self):
        with self.assertRaises(KeyError):
            core.mark_done([], 1)


class RemoveTodoTests(unittest.TestCase):
    def test_missing_id_raises_key_error(self):
        todos = [{"id": 1, "text": "a", "done": False}]
        with self.assertRaises(KeyError):
            core.remove_todo(todos, 99)

    def test_present_id_removes_only_that_item(self):
        todos = [
            {"id": 1, "text": "a", "done": False},
            {"id": 2, "text": "b", "done": False},
            {"id": 3, "text": "c", "done": False},
        ]
        result = core.remove_todo(todos, 2)
        self.assertEqual(
            result,
            [
                {"id": 1, "text": "a", "done": False},
                {"id": 3, "text": "c", "done": False},
            ],
        )

    def test_remove_todo_on_empty_list_raises_key_error(self):
        with self.assertRaises(KeyError):
            core.remove_todo([], 1)


class FormatListTests(unittest.TestCase):
    def test_two_todos(self):
        todos = [
            {"id": 1, "text": "a", "done": False},
            {"id": 2, "text": "b", "done": True},
        ]
        self.assertEqual(core.format_list(todos), "1 [ ] a\n2 [x] b")

    def test_empty_list_returns_empty_string(self):
        self.assertEqual(core.format_list([]), "")


if __name__ == "__main__":
    unittest.main()
