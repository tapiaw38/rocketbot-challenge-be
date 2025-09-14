"""
Additional tests for InMemoryTaskRepository using fixtures and edge cases.
"""

from datetime import datetime

import pytest

from src.core.domain.model import Task
from tests.conftest import (assert_task_equality,
                            assert_task_has_valid_timestamps)


class TestInMemoryTaskRepositoryWithFixtures:
    """Test suite using fixtures for more complex scenarios"""

    def test_create_task_with_fixture(self, empty_repository, sample_task):
        """Test task creation using fixtures"""

        created_task = empty_repository.create(sample_task)

        # Assert
        assert created_task.id == 1
        assert created_task.title == sample_task.title
        assert created_task.category == sample_task.category
        assert_task_has_valid_timestamps(created_task)

    def test_repository_with_preloaded_tasks(self, repository_with_tasks):
        """Test repository that comes pre-loaded with tasks"""
        repository, created_tasks = repository_with_tasks

        assert len(repository.find_all()) == 4
        assert len(created_tasks) == 4

        # Verify all tasks have correct IDs
        for i, task in enumerate(created_tasks, 1):
            assert task.id == i

    def test_find_tasks_by_category(self, repository_with_tasks):
        """Test finding tasks by category (custom logic test)"""
        repository, created_tasks = repository_with_tasks

        all_tasks = repository.find_all()
        work_tasks = [task for task in all_tasks if task.category == "Work"]
        personal_tasks = [task for task in all_tasks if task.category == "Personal"]

        assert len(work_tasks) == 2
        assert len(personal_tasks) == 2

        work_titles = [task.title for task in work_tasks]
        personal_titles = [task.title for task in personal_tasks]

        assert "Task 1" in work_titles
        assert "Task 3" in work_titles
        assert "Task 2" in personal_titles
        assert "Task 4" in personal_titles

    def test_task_builder_fixture(self, empty_repository, task_builder):
        """Test using the task builder fixture"""

        task = (
            task_builder()
            .with_title("Custom Built Task")
            .with_category("Custom Category")
            .build()
        )

        created_task = empty_repository.create(task)

        assert created_task.title == "Custom Built Task"
        assert created_task.category == "Custom Category"

    def test_bulk_operations(self, empty_repository, sample_tasks):
        """Test bulk operations on repository"""
        created_tasks = []
        for task in sample_tasks:
            created_task = empty_repository.create(task)
            created_tasks.append(created_task)

        assert len(empty_repository.find_all()) == len(sample_tasks)

        for task in created_tasks:
            updated_task_data = Task(
                title=f"Updated {task.title}", category=f"Updated {task.category}"
            )
            updated_task = empty_repository.update(task.id, updated_task_data)
            assert updated_task is not None
            assert updated_task.title.startswith("Updated")

        all_tasks = empty_repository.find_all()
        for task in all_tasks:
            assert task.title.startswith("Updated")
            assert task.category.startswith("Updated")

        tasks_to_delete = created_tasks[: len(created_tasks) // 2]
        for task in tasks_to_delete:
            result = empty_repository.delete(task.id)
            assert result is True

        remaining_tasks = empty_repository.find_all()
        assert len(remaining_tasks) == len(sample_tasks) - len(tasks_to_delete)


class TestInMemoryTaskRepositoryEdgeCases:
    """Test suite for edge cases and error conditions"""

    def test_create_task_with_empty_title(self, empty_repository):
        """Test creating task with empty title"""
        task = Task(title="", category="Test")

        created_task = empty_repository.create(task)

        assert created_task.title == ""
        assert created_task.id == 1

    def test_create_task_with_empty_category(self, empty_repository):
        """Test creating task with empty category"""
        task = Task(title="Test Task", category="")

        created_task = empty_repository.create(task)

        assert created_task.category == ""
        assert created_task.id == 1

    def test_create_task_with_very_long_strings(self, empty_repository):
        """Test creating task with very long title and category"""
        long_title = "A" * 1000
        long_category = "B" * 1000
        task = Task(title=long_title, category=long_category)

        created_task = empty_repository.create(task)

        assert created_task.title == long_title
        assert created_task.category == long_category
        assert len(created_task.title) == 1000
        assert len(created_task.category) == 1000

    def test_create_task_with_special_characters(self, empty_repository):
        """Test creating task with special characters"""
        special_title = "Task with émojis 🚀 and spécial charactérs !@#$%^&*()"
        special_category = "Catégory with unicode: αβγδε and symbols: ©®™"
        task = Task(title=special_title, category=special_category)

        created_task = empty_repository.create(task)

        assert created_task.title == special_title
        assert created_task.category == special_category

    def test_update_with_same_data(self, empty_repository):
        """Test updating task with exactly the same data"""
        original_task = Task(title="Original Task", category="Original")
        created_task = empty_repository.create(original_task)
        original_updated_at = created_task.updated_at

        import time

        time.sleep(0.001)

        same_task_data = Task(title="Original Task", category="Original")
        updated_task = empty_repository.update(created_task.id, same_task_data)

        assert updated_task is not None
        assert updated_task.title == "Original Task"
        assert updated_task.category == "Original"
        assert updated_task.updated_at > original_updated_at

    def test_delete_same_task_twice(self, empty_repository, sample_task):
        """Test deleting the same task twice"""
        created_task = empty_repository.create(sample_task)

        first_delete = empty_repository.delete(created_task.id)
        second_delete = empty_repository.delete(created_task.id)

        assert first_delete is True
        assert second_delete is False
        assert len(empty_repository.find_all()) == 0

    def test_operations_with_negative_ids(self, empty_repository):
        """Test operations with negative IDs"""
        assert empty_repository.find_by_id(-1) is None
        assert empty_repository.update(-1, Task(title="Test", category="Test")) is None
        assert empty_repository.delete(-1) is False

    def test_operations_with_zero_id(self, empty_repository):
        """Test operations with zero ID"""
        assert empty_repository.find_by_id(0) is None
        assert empty_repository.update(0, Task(title="Test", category="Test")) is None
        assert empty_repository.delete(0) is False

    def test_large_number_of_tasks(self, empty_repository):
        """Test repository with a large number of tasks"""
        num_tasks = 1000

        created_tasks = []
        for i in range(num_tasks):
            task = Task(title=f"Task {i}", category=f"Category {i % 10}")
            created_task = empty_repository.create(task)
            created_tasks.append(created_task)

        assert len(empty_repository.find_all()) == num_tasks
        assert empty_repository._next_id == num_tasks + 1

        middle_task = empty_repository.find_by_id(num_tasks // 2)
        assert middle_task is not None
        assert middle_task.title == f"Task {num_tasks // 2 - 1}"

        middle_id = num_tasks // 2
        assert empty_repository.delete(middle_id) is True
        assert len(empty_repository.find_all()) == num_tasks - 1
        assert empty_repository.find_by_id(middle_id) is None


class TestInMemoryTaskRepositoryPerformance:
    """Test suite for performance-related tests"""

    def test_find_by_id_performance_with_many_tasks(self, empty_repository):
        """Test that find_by_id performance is reasonable with many tasks"""
        import time

        num_tasks = 10000
        for i in range(num_tasks):
            task = Task(title=f"Task {i}", category="Performance Test")
            empty_repository.create(task)

        start_time = time.time()

        first_task = empty_repository.find_by_id(1)

        middle_task = empty_repository.find_by_id(num_tasks // 2)

        last_task = empty_repository.find_by_id(num_tasks)

        end_time = time.time()

        assert first_task is not None
        assert middle_task is not None
        assert last_task is not None

        elapsed_time = end_time - start_time
        assert (
            elapsed_time < 1.0
        ), f"Find operations took too long: {elapsed_time:.3f} seconds"

    def test_find_all_returns_copy_performance(self, empty_repository):
        """Test that find_all copy operation performance is reasonable"""
        import time

        num_tasks = 5000
        for i in range(num_tasks):
            task = Task(title=f"Task {i}", category="Performance Test")
            empty_repository.create(task)

        start_time = time.time()

        for _ in range(10):
            tasks = empty_repository.find_all()
            assert len(tasks) == num_tasks

        end_time = time.time()

        elapsed_time = end_time - start_time
        assert (
            elapsed_time < 1.0
        ), f"Multiple find_all operations took too long: {elapsed_time:.3f} seconds"
