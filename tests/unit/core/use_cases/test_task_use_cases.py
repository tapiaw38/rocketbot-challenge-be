import pytest
from unittest.mock import Mock, MagicMock
from datetime import datetime
from src.core.use_cases.task_use_cases import (
    CreateTaskUseCase,
    GetAllTasksUseCase,
    GetTaskByIdUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
)
from src.core.domain.model import Task
from src.core.platform.appcontext.appcontext import Context


class TestCreateTaskUseCase:
    """Test cases for CreateTaskUseCase"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository
        self.use_case = CreateTaskUseCase(self.mock_context)

    def test_create_task_success(self):
        """Test successful task creation"""
        title = "Test Task"
        category = "Testing"
        expected_task = Task(id=1, title=title, category=category)
        self.mock_repository.create.return_value = expected_task

        result = self.use_case.execute(title, category)

        assert result == expected_task
        self.mock_repository.create.assert_called_once()
        created_task = self.mock_repository.create.call_args[0][0]
        assert created_task.title == title
        assert created_task.category == category

    def test_create_task_with_empty_title(self):
        """Test task creation with empty title"""
        title = ""
        category = "Testing"
        expected_task = Task(id=1, title=title, category=category)
        self.mock_repository.create.return_value = expected_task

        result = self.use_case.execute(title, category)

        assert result == expected_task
        self.mock_repository.create.assert_called_once()

    def test_create_task_with_empty_category(self):
        """Test task creation with empty category"""
        title = "Test Task"
        category = ""
        expected_task = Task(id=1, title=title, category=category)
        self.mock_repository.create.return_value = expected_task

        result = self.use_case.execute(title, category)

        assert result == expected_task
        self.mock_repository.create.assert_called_once()


class TestGetAllTasksUseCase:
    """Test cases for GetAllTasksUseCase"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository
        self.use_case = GetAllTasksUseCase(self.mock_context)

    def test_get_all_tasks_empty_list(self):
        """Test getting all tasks when repository is empty"""

        self.mock_repository.find_all.return_value = []

        result = self.use_case.execute()

        assert result == []
        self.mock_repository.find_all.assert_called_once()

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks when repository has tasks"""

        task1 = Task(id=1, title="Task 1", category="Category 1")
        task2 = Task(id=2, title="Task 2", category="Category 2")
        expected_tasks = [task1, task2]
        self.mock_repository.find_all.return_value = expected_tasks

        result = self.use_case.execute()

        assert result == expected_tasks
        assert len(result) == 2
        self.mock_repository.find_all.assert_called_once()

    def test_get_all_tasks_returns_copy(self):
        """Test that get_all_tasks returns a copy of the repository data"""

        task = Task(id=1, title="Test Task", category="Testing")
        self.mock_repository.find_all.return_value = [task]

        result = self.use_case.execute()

        assert result == [task]
        self.mock_repository.find_all.assert_called_once()


class TestGetTaskByIdUseCase:
    """Test cases for GetTaskByIdUseCase"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository
        self.use_case = GetTaskByIdUseCase(self.mock_context)

    def test_get_task_by_id_existing_task(self):
        """Test getting an existing task by ID"""

        task_id = 1
        expected_task = Task(id=task_id, title="Test Task", category="Testing")
        self.mock_repository.find_by_id.return_value = expected_task

        result = self.use_case.execute(task_id)

        assert result == expected_task
        self.mock_repository.find_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_non_existing_task(self):
        """Test getting a non-existing task by ID"""

        task_id = 999
        self.mock_repository.find_by_id.return_value = None

        result = self.use_case.execute(task_id)

        assert result is None
        self.mock_repository.find_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_with_zero_id(self):
        """Test getting task with zero ID"""

        task_id = 0
        self.mock_repository.find_by_id.return_value = None

        result = self.use_case.execute(task_id)

        assert result is None
        self.mock_repository.find_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_with_negative_id(self):
        """Test getting task with negative ID"""

        task_id = -1
        self.mock_repository.find_by_id.return_value = None

        result = self.use_case.execute(task_id)

        assert result is None
        self.mock_repository.find_by_id.assert_called_once_with(task_id)


class TestUpdateTaskUseCase:
    """Test cases for UpdateTaskUseCase"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository
        self.use_case = UpdateTaskUseCase(self.mock_context)

    def test_update_task_success(self):
        """Test successful task update"""

        task_id = 1
        title = "Updated Task"
        category = "Updated Category"
        expected_task = Task(id=task_id, title=title, category=category)
        self.mock_repository.update.return_value = expected_task

        result = self.use_case.execute(task_id, title, category)

        assert result == expected_task
        self.mock_repository.update.assert_called_once()
        call_args = self.mock_repository.update.call_args
        assert call_args[0][0] == task_id
        updated_task = call_args[0][1]
        assert updated_task.title == title
        assert updated_task.category == category

    def test_update_task_non_existing(self):
        """Test updating a non-existing task"""

        task_id = 999
        title = "Updated Task"
        category = "Updated Category"
        self.mock_repository.update.return_value = None

        result = self.use_case.execute(task_id, title, category)

        assert result is None
        self.mock_repository.update.assert_called_once()

    def test_update_task_with_empty_title(self):
        """Test updating task with empty title"""

        task_id = 1
        title = ""
        category = "Updated Category"
        expected_task = Task(id=task_id, title=title, category=category)
        self.mock_repository.update.return_value = expected_task

        result = self.use_case.execute(task_id, title, category)

        assert result == expected_task
        self.mock_repository.update.assert_called_once()

    def test_update_task_with_empty_category(self):
        """Test updating task with empty category"""

        task_id = 1
        title = "Updated Task"
        category = ""
        expected_task = Task(id=task_id, title=title, category=category)
        self.mock_repository.update.return_value = expected_task

        result = self.use_case.execute(task_id, title, category)

        assert result == expected_task
        self.mock_repository.update.assert_called_once()


class TestDeleteTaskUseCase:
    """Test cases for DeleteTaskUseCase"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository
        self.use_case = DeleteTaskUseCase(self.mock_context)

    def test_delete_task_success(self):
        """Test successful task deletion"""

        task_id = 1
        self.mock_repository.delete.return_value = True

        result = self.use_case.execute(task_id)

        assert result is True
        self.mock_repository.delete.assert_called_once_with(task_id)

    def test_delete_task_non_existing(self):
        """Test deleting a non-existing task"""

        task_id = 999
        self.mock_repository.delete.return_value = False

        result = self.use_case.execute(task_id)

        assert result is False
        self.mock_repository.delete.assert_called_once_with(task_id)

    def test_delete_task_with_zero_id(self):
        """Test deleting task with zero ID"""

        task_id = 0
        self.mock_repository.delete.return_value = False

        result = self.use_case.execute(task_id)

        assert result is False
        self.mock_repository.delete.assert_called_once_with(task_id)

    def test_delete_task_with_negative_id(self):
        """Test deleting task with negative ID"""

        task_id = -1
        self.mock_repository.delete.return_value = False

        result = self.use_case.execute(task_id)

        assert result is False
        self.mock_repository.delete.assert_called_once_with(task_id)


class TestUseCasesIntegration:
    """Integration tests for use cases working together"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_context = Mock()
        self.mock_repository = Mock()
        self.mock_context.repositories.task = self.mock_repository

    def test_create_and_get_task_flow(self):
        """Test the flow of creating and then getting a task"""

        create_use_case = CreateTaskUseCase(self.mock_context)
        get_use_case = GetTaskByIdUseCase(self.mock_context)

        created_task = Task(id=1, title="Test Task", category="Testing")
        self.mock_repository.create.return_value = created_task
        self.mock_repository.find_by_id.return_value = created_task

        result_create = create_use_case.execute("Test Task", "Testing")
        result_get = get_use_case.execute(1)

        assert result_create == created_task
        assert result_get == created_task
        self.mock_repository.create.assert_called_once()
        self.mock_repository.find_by_id.assert_called_once_with(1)

    def test_create_update_delete_flow(self):
        """Test the flow of creating, updating, and deleting a task"""

        create_use_case = CreateTaskUseCase(self.mock_context)
        update_use_case = UpdateTaskUseCase(self.mock_context)
        delete_use_case = DeleteTaskUseCase(self.mock_context)

        created_task = Task(id=1, title="Test Task", category="Testing")
        updated_task = Task(id=1, title="Updated Task", category="Updated")

        self.mock_repository.create.return_value = created_task
        self.mock_repository.update.return_value = updated_task
        self.mock_repository.delete.return_value = True

        result_create = create_use_case.execute("Test Task", "Testing")
        result_update = update_use_case.execute(1, "Updated Task", "Updated")
        result_delete = delete_use_case.execute(1)

        assert result_create == created_task
        assert result_update == updated_task
        assert result_delete is True

        assert self.mock_repository.create.call_count == 1
        assert self.mock_repository.update.call_count == 1
        assert self.mock_repository.delete.call_count == 1
