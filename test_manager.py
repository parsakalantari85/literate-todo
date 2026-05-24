import os
import tempfile
import unittest
from manager import TodoList


class TestTodoList(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.tmp.close()
        os.unlink(self.tmp.name)  # let TodoList create it fresh
        self.todo = TodoList(filename=self.tmp.name)

    def tearDown(self):
        if os.path.exists(self.tmp.name):
            os.unlink(self.tmp.name)

    # --- add_task ---

    def test_add_task_returns_incrementing_ids(self):
        id1 = self.todo.add_task("First")
        id2 = self.todo.add_task("Second")
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_add_task_strips_whitespace(self):
        self.todo.add_task("  Buy milk  ")
        tasks = self.todo.get_tasks()
        self.assertEqual(tasks[0]['description'], "Buy milk")

    def test_add_task_empty_raises(self):
        with self.assertRaises(ValueError):
            self.todo.add_task("")

    def test_add_task_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            self.todo.add_task("   ")

    def test_add_task_stores_created_at(self):
        self.todo.add_task("Task with timestamp")
        tasks = self.todo.get_tasks()
        self.assertNotEqual(tasks[0]['created_at'], '')

    # --- get_tasks ---

    def test_get_tasks_empty(self):
        self.assertEqual(self.todo.get_tasks(), [])

    def test_get_tasks_returns_all(self):
        self.todo.add_task("A")
        self.todo.add_task("B")
        tasks = self.todo.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_new_task_is_not_completed(self):
        self.todo.add_task("Uncompleted task")
        tasks = self.todo.get_tasks()
        self.assertFalse(tasks[0]['completed'])

    # --- mark_completed ---

    def test_mark_completed(self):
        task_id = self.todo.add_task("Do laundry")
        self.todo.mark_completed(task_id)
        tasks = self.todo.get_tasks()
        self.assertTrue(tasks[0]['completed'])

    def test_mark_completed_invalid_id_raises(self):
        with self.assertRaises(ValueError):
            self.todo.mark_completed(999)

    # --- delete_task ---

    def test_delete_task(self):
        task_id = self.todo.add_task("Temporary task")
        self.todo.delete_task(task_id)
        self.assertEqual(self.todo.get_tasks(), [])

    def test_delete_task_invalid_id_raises(self):
        with self.assertRaises(ValueError):
            self.todo.delete_task(999)

    def test_delete_task_does_not_remove_others(self):
        id1 = self.todo.add_task("Keep me")
        id2 = self.todo.add_task("Delete me")
        self.todo.delete_task(id2)
        tasks = self.todo.get_tasks()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['id'], id1)

    # --- search_tasks ---

    def test_search_finds_matching_task(self):
        self.todo.add_task("Buy groceries")
        self.todo.add_task("Call dentist")
        results = self.todo.search_tasks("grocer")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['description'], "Buy groceries")

    def test_search_is_case_insensitive(self):
        self.todo.add_task("Read a Book")
        results = self.todo.search_tasks("book")
        self.assertEqual(len(results), 1)

    def test_search_empty_query_returns_empty(self):
        self.todo.add_task("Something")
        self.assertEqual(self.todo.search_tasks(""), [])

    def test_search_no_match_returns_empty(self):
        self.todo.add_task("Walk the dog")
        self.assertEqual(self.todo.search_tasks("xyz"), [])

    def test_search_matches_multiple(self):
        self.todo.add_task("Buy milk")
        self.todo.add_task("Buy eggs")
        self.todo.add_task("Call mom")
        results = self.todo.search_tasks("buy")
        self.assertEqual(len(results), 2)


if __name__ == '__main__':
    unittest.main()
