"""Unit tests for examples/todo-cli/todo.py.

Tests the public contract described in tasks/T-010.md (acceptance criteria),
not the implementation's internals. Exercises main(argv) directly, capturing
stdout/stderr, against a TODO_FILE pointed at a temp directory.
"""

import contextlib
import io
import json
import os
import tempfile
import unittest

import todo


class TodoCliTestCase(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._store_path = os.path.join(self._tmpdir.name, "todos.json")
        self._old_todo_file = os.environ.get("TODO_FILE")
        os.environ["TODO_FILE"] = self._store_path

    def tearDown(self):
        if self._old_todo_file is None:
            os.environ.pop("TODO_FILE", None)
        else:
            os.environ["TODO_FILE"] = self._old_todo_file
        self._tmpdir.cleanup()

    def _run(self, argv):
        out = io.StringIO()
        err = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = todo.main(argv)
        return code, out.getvalue(), err.getvalue()

    def _read_store(self):
        with open(self._store_path) as f:
            return json.load(f)


class AddCommandTests(TodoCliTestCase):
    def test_add_prints_id_writes_store_returns_0(self):
        code, out, err = self._run(["add", "buy milk"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1")
        self.assertEqual(err, "")
        self.assertTrue(os.path.exists(self._store_path))
        data = self._read_store()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["text"], "buy milk")
        self.assertFalse(data[0]["done"])

    def test_add_empty_text_errors_and_leaves_store_unchanged(self):
        # Seed the store with one existing todo first.
        self._run(["add", "existing"])
        before = self._read_store()

        code, out, err = self._run(["add", "   "])
        self.assertEqual(code, 1)
        self.assertEqual(out, "")
        self.assertNotEqual(err, "")

        after = self._read_store()
        self.assertEqual(before, after)

    def test_add_on_pristine_empty_text_store_stays_absent_or_empty(self):
        code, out, err = self._run(["add", ""])
        self.assertEqual(code, 1)
        self.assertNotEqual(err, "")
        # No store file should have been written since add_todo raised
        # before storage.save was ever called.
        self.assertFalse(os.path.exists(self._store_path))


class ListCommandTests(TodoCliTestCase):
    def test_list_empty_store_prints_nothing_returns_0(self):
        code, out, err = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "")
        self.assertEqual(err, "")

    def test_list_prints_expected_format(self):
        self._run(["add", "buy milk"])
        code, out, err = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1 [ ] buy milk")

    def test_list_does_not_write_store(self):
        self._run(["add", "buy milk"])
        before_mtime = os.path.getmtime(self._store_path)
        self._run(["list"])
        after_mtime = os.path.getmtime(self._store_path)
        self.assertEqual(before_mtime, after_mtime)


class DoneCommandTests(TodoCliTestCase):
    def test_done_marks_todo_done_returns_0(self):
        self._run(["add", "buy milk"])
        code, out, err = self._run(["done", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        data = self._read_store()
        self.assertTrue(data[0]["done"])

    def test_done_unknown_id_errors_returns_1(self):
        code, out, err = self._run(["done", "42"])
        self.assertEqual(code, 1)
        self.assertNotEqual(err, "")


class RmCommandTests(TodoCliTestCase):
    def test_rm_removes_todo_returns_0(self):
        self._run(["add", "buy milk"])
        code, out, err = self._run(["rm", "1"])
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        data = self._read_store()
        self.assertEqual(data, [])

    def test_rm_unknown_id_errors_returns_1(self):
        code, out, err = self._run(["rm", "99"])
        self.assertEqual(code, 1)
        self.assertNotEqual(err, "")


class CorruptStoreTests(TodoCliTestCase):
    def test_corrupt_store_returns_2(self):
        with open(self._store_path, "w") as f:
            f.write("{not valid json")

        code, out, err = self._run(["list"])
        self.assertEqual(code, 2)
        self.assertNotEqual(err, "")

    def test_corrupt_store_schema_mismatch_returns_2(self):
        with open(self._store_path, "w") as f:
            json.dump([{"id": 1, "text": "x"}], f)  # missing "done" key

        code, out, err = self._run(["add", "another"])
        self.assertEqual(code, 2)
        self.assertNotEqual(err, "")


class ArgparseTypeIntTests(TodoCliTestCase):
    def test_done_non_integer_id_raises_systemexit(self):
        with self.assertRaises(SystemExit):
            todo.main(["done", "abc"])

    def test_rm_non_integer_id_raises_systemexit(self):
        with self.assertRaises(SystemExit):
            todo.main(["rm", "abc"])


class RoundTripTests(TodoCliTestCase):
    def test_full_round_trip(self):
        # add
        code, out, err = self._run(["add", "buy milk"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1")

        # list -> one item, not done
        code, out, err = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1 [ ] buy milk")

        # done
        code, out, err = self._run(["done", "1"])
        self.assertEqual(code, 0)

        # list -> one item, done
        code, out, err = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "1 [x] buy milk")

        # rm
        code, out, err = self._run(["rm", "1"])
        self.assertEqual(code, 0)

        # list -> empty again
        code, out, err = self._run(["list"])
        self.assertEqual(code, 0)
        self.assertEqual(out, "")

        # store file itself reflects final empty state
        self.assertEqual(self._read_store(), [])


if __name__ == "__main__":
    unittest.main()
