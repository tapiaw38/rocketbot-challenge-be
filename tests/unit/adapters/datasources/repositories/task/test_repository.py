"""
Tests for InMemoryTaskRepository

This module contains comprehensive unit tests for the InMemoryTaskRepository class,
testing all CRUD operations and edge cases.
"""

from datetime import datetime
from typing import List, Optional

import pytest

from src.adapters.datasources.repositories.task.repository import \
    InMemoryTaskRepository
from src.adapters.datasources.repositories.task.repository_interface import \
    TaskRepositoryInterface
from src.core.domain.model import Task


class TestInMemoryTaskRepository:
    """Test suite for InMemoryTaskRepository"""

    def setup_method(self):
        """Set up test fixtures before each test method"""
        self.repository = InMemoryTaskRepository()

    def test_implements_repository_interface(self):
        """Test that InMemoryTaskRepository implements TaskRepositoryInterface"""
        assert isinstance(self.repository, TaskRepositoryInterface)

    def test_initial_state(self):
        """Test repository initial state"""
        assert self.repository._tasks == []
        assert self.repository._next_id == 1

    def test_create_task_success(self):
        """Test successful task creation"""
        task = Task(title="Test Task", category="Testing")

        created_task = self.repository.create(task)

        assert created_task.id == 1
        assert created_task.title == "Test Task"
        assert created_task.category == "Testing"
        assert created_task.created_at is not None
        assert created_task.updated_at is not None
        assert isinstance(created_task.created_at, datetime)
        assert isinstance(created_task.updated_at, datetime)

        assert len(self.repository._tasks) == 1
        assert self.repository._tasks[0] == created_task

    def test_create_multiple_tasks_increments_id(self):
        """Test that creating multiple tasks increments ID correctly"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")
        task3 = Task(title="Task 3", category="Category 3")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)
        created_task3 = self.repository.create(task3)

        assert created_task1.id == 1
        assert created_task2.id == 2
        assert created_task3.id == 3
        assert self.repository._next_id == 4
        assert len(self.repository._tasks) == 3

    def test_find_all_empty_repository(self):
        """Test find_all returns empty list when repository is empty"""
        tasks = self.repository.find_all()

        assert tasks == []
        assert isinstance(tasks, list)

    def test_find_all_with_tasks(self):
        """Test find_all returns all tasks"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)

        tasks = self.repository.find_all()

        assert len(tasks) == 2
        assert created_task1 in tasks
        assert created_task2 in tasks

    def test_find_all_returns_copy(self):
        """Test that find_all returns a copy, not the original list"""
        task = Task(title="Test Task", category="Testing")
        self.repository.create(task)

        tasks = self.repository.find_all()
        tasks.append(Task(title="External Task", category="External"))

        assert len(self.repository._tasks) == 1
        assert len(tasks) == 2

    def test_find_by_id_existing_task(self):
        """Test finding an existing task by ID"""
        task = Task(title="Test Task", category="Testing")
        created_task = self.repository.create(task)

        found_task = self.repository.find_by_id(created_task.id)

        assert found_task is not None
        assert found_task.id == created_task.id
        assert found_task.title == created_task.title
        assert found_task.category == created_task.category

    def test_find_by_id_non_existing_task(self):
        """Test finding a non-existing task by ID"""
        found_task = self.repository.find_by_id(999)

        assert found_task is None

    def test_find_by_id_with_multiple_tasks(self):
        """Test finding specific task by ID when multiple tasks exist"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")
        task3 = Task(title="Task 3", category="Category 3")

        self.repository.create(task1)
        self.repository.create(task2)
        self.repository.create(task3)

        found_task2 = self.repository.find_by_id(2)
        assert found_task2 is not None
        assert found_task2.id == 2
        assert found_task2.title == "Task 2"

    def test_update_existing_task(self):
        """Test updating an existing task"""
        original_task = Task(title="Original Task", category="Original")
        created_task = self.repository.create(original_task)
        original_created_at = created_task.created_at

        import time

        time.sleep(0.001)

        updated_task_data = Task(title="Updated Task", category="Updated")
        updated_task = self.repository.update(created_task.id, updated_task_data)

        assert updated_task is not None
        assert updated_task.id == created_task.id
        assert updated_task.title == "Updated Task"
        assert updated_task.category == "Updated"
        assert updated_task.created_at == original_created_at
        assert updated_task.updated_at != original_created_at
        assert updated_task.updated_at > original_created_at

    def test_update_non_existing_task(self):
        """Test updating a non-existing task"""
        updated_task_data = Task(title="Updated Task", category="Updated")

        updated_task = self.repository.update(999, updated_task_data)

        assert updated_task is None

    def test_update_preserves_other_tasks(self):
        """Test that updating one task doesn't affect others"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)

        updated_task_data = Task(title="Updated Task 1", category="Updated Category 1")
        self.repository.update(created_task1.id, updated_task_data)

        found_task2 = self.repository.find_by_id(created_task2.id)
        assert found_task2.title == "Task 2"
        assert found_task2.category == "Category 2"

    def test_delete_existing_task(self):
        """Test deleting an existing task"""
        task = Task(title="Test Task", category="Testing")
        created_task = self.repository.create(task)

        result = self.repository.delete(created_task.id)

        assert result is True
        assert len(self.repository._tasks) == 0
        assert self.repository.find_by_id(created_task.id) is None

    def test_delete_non_existing_task(self):
        """Test deleting a non-existing task"""
        result = self.repository.delete(999)

        assert result is False

    def test_delete_preserves_other_tasks(self):
        """Test that deleting one task doesn't affect others"""
        task1 = Task(title="Task 1", category="Category 1")
        task2 = Task(title="Task 2", category="Category 2")
        task3 = Task(title="Task 3", category="Category 3")

        created_task1 = self.repository.create(task1)
        created_task2 = self.repository.create(task2)
        created_task3 = self.repository.create(task3)

        result = self.repository.delete(created_task2.id)

        assert result is True
        assert len(self.repository._tasks) == 2

        remaining_tasks = self.repository.find_all()
        remaining_ids = [task.id for task in remaining_tasks]
        assert created_task1.id in remaining_ids
        assert created_task3.id in remaining_ids
        assert created_task2.id not in remaining_ids

    def test_delete_from_empty_repository(self):
        """Test deleting from empty repository"""
        result = self.repository.delete(1)

        assert result is False
        assert len(self.repository._tasks) == 0

    def test_complex_crud_operations_sequence(self):
        """Test a complex sequence of CRUD operations"""
        task1 = self.repository.create(Task(title="Task 1", category="Work"))
        task2 = self.repository.create(Task(title="Task 2", category="Personal"))
        task3 = self.repository.create(Task(title="Task 3", category="Work"))

        assert len(self.repository.find_all()) == 3

        updated_task2 = self.repository.update(
            task2.id, Task(title="Updated Task 2", category="Personal Updated")
        )
        assert updated_task2.title == "Updated Task 2"

        assert self.repository.delete(task1.id) is True
        assert len(self.repository.find_all()) == 2

        remaining_tasks = self.repository.find_all()
        remaining_ids = [task.id for task in remaining_tasks]
        assert task2.id in remaining_ids
        assert task3.id in remaining_ids
        assert task1.id not in remaining_ids

        assert self.repository.find_by_id(task1.id) is None

        found_task2 = self.repository.find_by_id(task2.id)
        found_task3 = self.repository.find_by_id(task3.id)

        assert found_task2.title == "Updated Task 2"
        assert found_task3.title == "Task 3"

    def test_task_timestamps_are_set_correctly(self):
        """Test that timestamps are set correctly on create and update"""
        task = Task(title="Test Task", category="Testing")
        before_create = datetime.now()
        created_task = self.repository.create(task)
        after_create = datetime.now()

        assert before_create <= created_task.created_at <= after_create
        assert before_create <= created_task.updated_at <= after_create
        assert created_task.created_at == created_task.updated_at

        import time

        time.sleep(0.001)

        updated_task_data = Task(title="Updated Task", category="Updated")
        before_update = datetime.now()
        updated_task = self.repository.update(created_task.id, updated_task_data)
        after_update = datetime.now()

        assert updated_task.created_at == created_task.created_at  # Should not change
        assert before_update <= updated_task.updated_at <= after_update
        assert updated_task.updated_at > updated_task.created_at

    def test_repository_isolation(self):
        """Test that multiple repository instances are isolated"""
        repo1 = InMemoryTaskRepository()
        repo2 = InMemoryTaskRepository()

        task1 = repo1.create(Task(title="Task in Repo 1", category="Repo1"))
        task2 = repo2.create(Task(title="Task in Repo 2", category="Repo2"))

        assert len(repo1.find_all()) == 1
        assert len(repo2.find_all()) == 1
        assert repo1.find_by_id(task1.id) == task1
        assert repo2.find_by_id(task2.id) == task2

        assert repo1.find_by_id(task2.id) is None or repo1.find_by_id(task2.id) != task2
        assert repo2.find_by_id(task1.id) is None or repo2.find_by_id(task1.id) != task1
