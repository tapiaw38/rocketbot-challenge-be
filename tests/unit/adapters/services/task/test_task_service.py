import pytest
from unittest.mock import Mock, AsyncMock
from datetime import datetime
from src.adapters.services.task.task_service import TaskService
from src.core.use_cases.use_cases import Usecases, Task
from src.core.use_cases.task_use_cases import (
    CreateTaskUseCase,
    GetAllTasksUseCase,
    GetTaskByIdUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
)
from src.schemas.schemas import TaskInput, TaskOutput, DeleteTaskResponse
from src.core.domain.model import Task as DomainTask


class TestTaskService:
    """Test cases for TaskService"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_create_usecase = Mock(spec=CreateTaskUseCase)
        self.mock_get_all_usecase = Mock(spec=GetAllTasksUseCase)
        self.mock_get_by_id_usecase = Mock(spec=GetTaskByIdUseCase)
        self.mock_update_usecase = Mock(spec=UpdateTaskUseCase)
        self.mock_delete_usecase = Mock(spec=DeleteTaskUseCase)

        self.mock_task_usecases = Mock(spec=Task)
        self.mock_task_usecases.create_usecase = self.mock_create_usecase
        self.mock_task_usecases.get_all_usecase = self.mock_get_all_usecase
        self.mock_task_usecases.get_by_id_usecase = self.mock_get_by_id_usecase
        self.mock_task_usecases.update_usecase = self.mock_update_usecase
        self.mock_task_usecases.delete_usecase = self.mock_delete_usecase

        self.mock_usecases = Mock(spec=Usecases)
        self.mock_usecases.task = self.mock_task_usecases

        self.service = TaskService(self.mock_usecases)

    async def test_create_task_success(self):
        """Test successful task creation"""
        task_input = TaskInput(title="Test Task", category="Testing")
        domain_task = DomainTask(id=1, title="Test Task", category="Testing")
        self.mock_create_usecase.execute.return_value = domain_task

        result = await self.service.create_task(task_input)

        assert isinstance(result, TaskOutput)
        assert result.id == 1
        assert result.title == "Test Task"
        assert result.category == "Testing"
        self.mock_create_usecase.execute.assert_called_once_with(
            title="Test Task", category="Testing"
        )

    async def test_create_task_with_empty_title(self):
        """Test task creation with empty title"""
        task_input = TaskInput(title="", category="Testing")
        domain_task = DomainTask(id=1, title="", category="Testing")
        self.mock_create_usecase.execute.return_value = domain_task

        result = await self.service.create_task(task_input)

        assert isinstance(result, TaskOutput)
        assert result.title == ""
        self.mock_create_usecase.execute.assert_called_once_with(
            title="", category="Testing"
        )

    async def test_create_task_with_empty_category(self):
        """Test task creation with empty category"""
        task_input = TaskInput(title="Test Task", category="")
        domain_task = DomainTask(id=1, title="Test Task", category="")
        self.mock_create_usecase.execute.return_value = domain_task

        result = await self.service.create_task(task_input)

        assert isinstance(result, TaskOutput)
        assert result.category == ""
        self.mock_create_usecase.execute.assert_called_once_with(
            title="Test Task", category=""
        )

    async def test_get_all_tasks_success(self):
        """Test successful get all tasks"""
        task1 = DomainTask(id=1, title="Task 1", category="Category 1")
        task2 = DomainTask(id=2, title="Task 2", category="Category 2")
        self.mock_get_all_usecase.execute.return_value = [task1, task2]

        result = await self.service.get_all_tasks()

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(task, TaskOutput) for task in result)
        assert result[0].id == 1
        assert result[0].title == "Task 1"
        assert result[1].id == 2
        assert result[1].title == "Task 2"
        self.mock_get_all_usecase.execute.assert_called_once()

    async def test_get_all_tasks_empty_list(self):
        """Test get all tasks when no tasks exist"""
        self.mock_get_all_usecase.execute.return_value = []

        result = await self.service.get_all_tasks()

        assert isinstance(result, list)
        assert len(result) == 0
        self.mock_get_all_usecase.execute.assert_called_once()

    async def test_get_task_by_id_success(self):
        """Test successful get task by ID"""
        task_id = 1
        domain_task = DomainTask(id=task_id, title="Test Task", category="Testing")
        self.mock_get_by_id_usecase.execute.return_value = domain_task

        result = await self.service.get_task_by_id(task_id)

        assert isinstance(result, TaskOutput)
        assert result.id == task_id
        assert result.title == "Test Task"
        assert result.category == "Testing"
        self.mock_get_by_id_usecase.execute.assert_called_once_with(task_id)

    async def test_get_task_by_id_not_found(self):
        """Test get task by ID when task doesn't exist"""
        task_id = 999
        self.mock_get_by_id_usecase.execute.return_value = None

        result = await self.service.get_task_by_id(task_id)

        assert result is None
        self.mock_get_by_id_usecase.execute.assert_called_once_with(task_id)

    async def test_get_task_by_id_with_zero_id(self):
        """Test get task by ID with zero ID"""
        task_id = 0
        self.mock_get_by_id_usecase.execute.return_value = None

        result = await self.service.get_task_by_id(task_id)

        assert result is None
        self.mock_get_by_id_usecase.execute.assert_called_once_with(task_id)

    async def test_get_task_by_id_with_negative_id(self):
        """Test get task by ID with negative ID"""
        task_id = -1
        self.mock_get_by_id_usecase.execute.return_value = None

        result = await self.service.get_task_by_id(task_id)

        assert result is None
        self.mock_get_by_id_usecase.execute.assert_called_once_with(task_id)

    async def test_update_task_success(self):
        """Test successful task update"""
        task_id = 1
        task_input = TaskInput(title="Updated Task", category="Updated Category")
        domain_task = DomainTask(
            id=task_id, title="Updated Task", category="Updated Category"
        )
        self.mock_update_usecase.execute.return_value = domain_task

        result = await self.service.update_task(task_id, task_input)

        assert isinstance(result, TaskOutput)
        assert result.id == task_id
        assert result.title == "Updated Task"
        assert result.category == "Updated Category"
        self.mock_update_usecase.execute.assert_called_once_with(
            task_id=task_id, title="Updated Task", category="Updated Category"
        )

    async def test_update_task_not_found(self):
        """Test update task when task doesn't exist"""
        task_id = 999
        task_input = TaskInput(title="Updated Task", category="Updated Category")
        self.mock_update_usecase.execute.return_value = None

        result = await self.service.update_task(task_id, task_input)

        assert result is None
        self.mock_update_usecase.execute.assert_called_once_with(
            task_id=task_id, title="Updated Task", category="Updated Category"
        )

    async def test_update_task_with_empty_data(self):
        """Test update task with empty title and category"""
        task_id = 1
        task_input = TaskInput(title="", category="")
        domain_task = DomainTask(id=task_id, title="", category="")
        self.mock_update_usecase.execute.return_value = domain_task

        result = await self.service.update_task(task_id, task_input)

        assert isinstance(result, TaskOutput)
        assert result.title == ""
        assert result.category == ""
        self.mock_update_usecase.execute.assert_called_once_with(
            task_id=task_id, title="", category=""
        )

    async def test_delete_task_success(self):
        """Test successful task deletion"""
        task_id = 1
        self.mock_delete_usecase.execute.return_value = True

        result = await self.service.delete_task(task_id)

        assert isinstance(result, DeleteTaskResponse)
        assert result.message == f"Task {task_id} eliminada correctamente"
        self.mock_delete_usecase.execute.assert_called_once_with(task_id)

    async def test_delete_task_not_found(self):
        """Test delete task when task doesn't exist"""
        task_id = 999
        self.mock_delete_usecase.execute.return_value = False

        result = await self.service.delete_task(task_id)

        assert isinstance(result, DeleteTaskResponse)
        assert result.message == f"Task {task_id} no encontrada"
        self.mock_delete_usecase.execute.assert_called_once_with(task_id)

    async def test_delete_task_with_zero_id(self):
        """Test delete task with zero ID"""
        task_id = 0
        self.mock_delete_usecase.execute.return_value = False

        result = await self.service.delete_task(task_id)

        assert isinstance(result, DeleteTaskResponse)
        assert result.message == f"Task {task_id} no encontrada"
        self.mock_delete_usecase.execute.assert_called_once_with(task_id)

    async def test_delete_task_with_negative_id(self):
        """Test delete task with negative ID"""
        task_id = -1
        self.mock_delete_usecase.execute.return_value = False

        result = await self.service.delete_task(task_id)

        assert isinstance(result, DeleteTaskResponse)
        assert result.message == f"Task {task_id} no encontrada"
        self.mock_delete_usecase.execute.assert_called_once_with(task_id)


class TestTaskServiceIntegration:
    """Integration tests for TaskService with use cases"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_create_usecase = Mock(spec=CreateTaskUseCase)
        self.mock_get_all_usecase = Mock(spec=GetAllTasksUseCase)
        self.mock_get_by_id_usecase = Mock(spec=GetTaskByIdUseCase)
        self.mock_update_usecase = Mock(spec=UpdateTaskUseCase)
        self.mock_delete_usecase = Mock(spec=DeleteTaskUseCase)

        self.mock_task_usecases = Mock(spec=Task)
        self.mock_task_usecases.create_usecase = self.mock_create_usecase
        self.mock_task_usecases.get_all_usecase = self.mock_get_all_usecase
        self.mock_task_usecases.get_by_id_usecase = self.mock_get_by_id_usecase
        self.mock_task_usecases.update_usecase = self.mock_update_usecase
        self.mock_task_usecases.delete_usecase = self.mock_delete_usecase

        self.mock_usecases = Mock(spec=Usecases)
        self.mock_usecases.task = self.mock_task_usecases

        self.service = TaskService(self.mock_usecases)

    async def test_create_and_get_task_flow(self):
        """Test the flow of creating and then getting a task"""
        task_input = TaskInput(title="Test Task", category="Testing")
        domain_task = DomainTask(id=1, title="Test Task", category="Testing")
        self.mock_create_usecase.execute.return_value = domain_task
        self.mock_get_by_id_usecase.execute.return_value = domain_task

        created_result = self.service.create_task(task_input)
        retrieved_result = self.service.get_task_by_id(1)

        assert isinstance(created_result, TaskOutput)
        assert isinstance(retrieved_result, TaskOutput)
        assert created_result.id == retrieved_result.id
        assert created_result.title == retrieved_result.title
        assert created_result.category == retrieved_result.category

    async def test_create_update_delete_flow(self):
        """Test the flow of creating, updating, and deleting a task"""
        create_input = TaskInput(title="Test Task", category="Testing")
        update_input = TaskInput(title="Updated Task", category="Updated")

        created_task = DomainTask(id=1, title="Test Task", category="Testing")
        updated_task = DomainTask(id=1, title="Updated Task", category="Updated")

        self.mock_create_usecase.execute.return_value = created_task
        self.mock_update_usecase.execute.return_value = updated_task
        self.mock_delete_usecase.execute.return_value = True

        create_result = self.service.create_task(create_input)
        update_result = self.service.update_task(1, update_input)
        delete_result = self.service.delete_task(1)

        assert isinstance(create_result, TaskOutput)
        assert isinstance(update_result, TaskOutput)
        assert isinstance(delete_result, DeleteTaskResponse)

        assert create_result.title == "Test Task"
        assert update_result.title == "Updated Task"
        assert delete_result.message == "Task 1 eliminada correctamente"

    async def test_task_output_from_task_with_timestamps(self):
        """Test TaskOutput.from_task method with timestamps"""
        now = datetime.now()
        domain_task = DomainTask(
            id=1, title="Test Task", category="Testing", created_at=now, updated_at=now
        )
        self.mock_create_usecase.execute.return_value = domain_task

        task_input = TaskInput(title="Test Task", category="Testing")
        result = await self.service.create_task(task_input)

        assert isinstance(result, TaskOutput)
        assert result.created_at == now.isoformat()
        assert result.updated_at == now.isoformat()

    async def test_task_output_from_task_without_timestamps(self):
        """Test TaskOutput.from_task method without timestamps"""
        domain_task = DomainTask(
            id=1,
            title="Test Task",
            category="Testing",
            created_at=None,
            updated_at=None,
        )
        self.mock_create_usecase.execute.return_value = domain_task

        task_input = TaskInput(title="Test Task", category="Testing")
        result = await self.service.create_task(task_input)

        assert isinstance(result, TaskOutput)
        assert result.created_at is None
        assert result.updated_at is None
