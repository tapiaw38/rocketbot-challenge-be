#!/usr/bin/env python3
"""
Simple test runner that doesn't require pytest to be globally installed.
This script can be used to run tests using Python's built-in unittest framework.
"""

import os
import sys
import unittest
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from adapters.datasources.repositories.task.repository import InMemoryTaskRepository
from core.domain.model import Task


class TestInMemoryTaskRepositoryBasic(unittest.TestCase):
    """Basic tests for InMemoryTaskRepository using unittest"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        self.repository = InMemoryTaskRepository()

    def test_create_task(self):
        """Test task creation"""
        task = Task(title="Test Task", category="Testing")
        created_task = self.repository.create(task)

        self.assertEqual(created_task.id, 1)
        self.assertEqual(created_task.title, "Test Task")
        self.assertEqual(created_task.category, "Testing")
        self.assertIsNotNone(created_task.created_at)
        self.assertIsNotNone(created_task.updated_at)

    def test_find_all_empty(self):
        """Test find_all on empty repository"""
        tasks = self.repository.find_all()
        self.assertEqual(tasks, [])

    def test_find_all_with_tasks(self):
        """Test find_all with tasks"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)

        tasks = self.repository.find_all()
        self.assertEqual(len(tasks), 2)
        self.assertIn(created_task1, tasks)
        self.assertIn(created_task2, tasks)

    def test_find_by_id_existing(self):
        """Test finding existing task by ID"""
        task = Task(title="Test Task", category="Testing")
        created_task = self.repository.create(task)

        found_task = self.repository.find_by_id(created_task.id)
        self.assertIsNotNone(found_task)
        self.assertEqual(found_task.id, created_task.id)
        self.assertEqual(found_task.title, created_task.title)

    def test_find_by_id_non_existing(self):
        """Test finding non-existing task by ID"""
        found_task = self.repository.find_by_id(999)
        self.assertIsNone(found_task)

    def test_update_existing_task(self):
        """Test updating existing task"""
        original_task = Task(title="Original", category="Original")
        created_task = self.repository.create(original_task)

        updated_task_data = Task(title="Updated", category="Updated")
        updated_task = self.repository.update(created_task.id, updated_task_data)

        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.title, "Updated")
        self.assertEqual(updated_task.category, "Updated")
        self.assertEqual(updated_task.id, created_task.id)

    def test_update_non_existing_task(self):
        """Test updating non-existing task"""
        updated_task_data = Task(title="Updated", category="Updated")
        updated_task = self.repository.update(999, updated_task_data)

        self.assertIsNone(updated_task)

    def test_delete_existing_task(self):
        """Test deleting existing task"""
        task = Task(title="Test Task", category="Testing")
        created_task = self.repository.create(task)

        result = self.repository.delete(created_task.id)

        self.assertTrue(result)
        self.assertEqual(len(self.repository.find_all()), 0)

    def test_delete_non_existing_task(self):
        """Test deleting non-existing task"""
        result = self.repository.delete(999)
        self.assertFalse(result)

    def test_id_increment(self):
        """Test that IDs increment correctly"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)

        self.assertEqual(created_task1.id, 1)
        self.assertEqual(created_task2.id, 2)

    def test_complex_workflow(self):
        """Test a complex workflow of operations"""
        task1 = self.repository.create(Task(title="Task 1", category="Work"))
        task2 = self.repository.create(Task(title="Task 2", category="Personal"))

        self.assertEqual(len(self.repository.find_all()), 2)

        updated_task = self.repository.update(
            task1.id, Task(title="Updated Task 1", category="Work Updated")
        )
        self.assertEqual(updated_task.title, "Updated Task 1")

        self.assertTrue(self.repository.delete(task2.id))
        self.assertEqual(len(self.repository.find_all()), 1)

        remaining_tasks = self.repository.find_all()
        self.assertEqual(remaining_tasks[0].title, "Updated Task 1")


if __name__ == "__main__":
    unittest.main(verbosity=2)
