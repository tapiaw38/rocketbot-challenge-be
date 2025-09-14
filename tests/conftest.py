"""
Test fixtures and configuration for the test suite.
"""

from datetime import datetime
from typing import List

import pytest

from src.adapters.datasources.repositories.task.repository import \
    InMemoryTaskRepository
from src.core.domain.model import Task


@pytest.fixture
def empty_repository():
    """Fixture that provides a fresh empty repository for each test"""
    return InMemoryTaskRepository()


@pytest.fixture
def sample_task():
    """Fixture that provides a sample task for testing"""
    return Task(title="Sample Task", category="Sample Category")


@pytest.fixture
def sample_tasks():
    """Fixture that provides a list of sample tasks for testing"""
    return [
        Task(title="Task 1", category="Work"),
        Task(title="Task 2", category="Personal"),
        Task(title="Task 3", category="Work"),
        Task(title="Task 4", category="Personal"),
    ]


@pytest.fixture
def repository_with_tasks(empty_repository, sample_tasks):
    """Fixture that provides a repository pre-populated with sample tasks"""
    repository = empty_repository
    created_tasks = []

    for task in sample_tasks:
        created_task = repository.create(task)
        created_tasks.append(created_task)

    return repository, created_tasks


@pytest.fixture
def task_data():
    """Fixture that provides task data for creation"""
    return {"title": "Test Task", "category": "Testing"}


class TaskBuilder:
    """Builder pattern for creating test tasks with various configurations"""

    def __init__(self):
        self.title = "Default Task"
        self.category = "Default Category"

    def with_title(self, title: str):
        self.title = title
        return self

    def with_category(self, category: str):
        self.category = category
        return self

    def build(self) -> Task:
        return Task(title=self.title, category=self.category)


@pytest.fixture
def task_builder():
    """Fixture that provides a TaskBuilder for flexible task creation"""
    return TaskBuilder


def assert_task_equality(task1: Task, task2: Task, ignore_timestamps: bool = False):
    """Helper function to assert task equality with optional timestamp ignoring"""
    assert task1.id == task2.id
    assert task1.title == task2.title
    assert task1.category == task2.category

    if not ignore_timestamps:
        assert task1.created_at == task2.created_at
        assert task1.updated_at == task2.updated_at


def assert_task_has_valid_timestamps(task: Task):
    """Helper function to assert that a task has valid timestamps"""
    assert task.created_at is not None
    assert task.updated_at is not None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)
    assert task.created_at <= task.updated_at
