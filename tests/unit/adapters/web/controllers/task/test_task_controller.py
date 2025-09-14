from datetime import datetime
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from src.adapters.services.task.task_service import TaskService
from src.adapters.web.controllers.task.task_controller import get_task_service, router
from src.core.domain.model import Task
from src.schemas.schemas import DeleteTaskResponse, TaskInput, TaskOutput


class TestTaskController:
    """Test cases for TaskController endpoints"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_service = Mock(spec=TaskService)
        self.mock_service.create_task = AsyncMock()
        self.mock_service.get_all_tasks = AsyncMock()
        self.mock_service.get_task_by_id = AsyncMock()
        self.mock_service.update_task = AsyncMock()
        self.mock_service.delete_task = AsyncMock()

    def _create_test_app(self):
        """Helper method to create test app with dependency override"""
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_task_service] = lambda: self.mock_service
        return TestClient(app)

    def test_get_task_service_dependency_error(self):
        """Test that get_task_service dependency raises HTTPException"""
        with pytest.raises(HTTPException) as exc_info:
            get_task_service()

        assert exc_info.value.status_code == 500
        assert exc_info.value.detail == "Service not configured"

    def test_get_all_tasks_success(self):
        """Test successful get all tasks endpoint"""
        task1 = TaskOutput(id=1, title="Task 1", category="Category 1")
        task2 = TaskOutput(id=2, title="Task 2", category="Category 2")
        self.mock_service.get_all_tasks.return_value = [task1, task2]

        client = self._create_test_app()
        response = client.get("/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["title"] == "Task 1"
        assert data[1]["id"] == 2
        assert data[1]["title"] == "Task 2"
        self.mock_service.get_all_tasks.assert_called_once()

    def test_get_all_tasks_empty_list(self):
        """Test get all tasks when no tasks exist"""
        self.mock_service.get_all_tasks.return_value = []

        client = self._create_test_app()
        response = client.get("/tasks/")

        assert response.status_code == 200
        data = response.json()
        assert data == []
        self.mock_service.get_all_tasks.assert_called_once()

    def test_create_task_success(self):
        """Test successful task creation endpoint"""
        task_input = TaskInput(title="New Task", category="New Category")
        created_task = TaskOutput(id=1, title="New Task", category="New Category")
        self.mock_service.create_task.return_value = created_task

        client = self._create_test_app()
        response = client.post("/tasks/", json=task_input.model_dump())

        assert response.status_code == 201
        data = response.json()
        assert data["id"] == 1
        assert data["title"] == "New Task"
        assert data["category"] == "New Category"
        self.mock_service.create_task.assert_called_once()

    def test_create_task_with_empty_title(self):
        """Test task creation with empty title"""
        task_input = TaskInput(title="", category="Category")
        created_task = TaskOutput(id=1, title="", category="Category")
        self.mock_service.create_task.return_value = created_task

        client = self._create_test_app()
        response = client.post("/tasks/", json=task_input.model_dump())

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == ""
        self.mock_service.create_task.assert_called_once()

    def test_create_task_with_empty_category(self):
        """Test task creation with empty category"""
        task_input = TaskInput(title="Task Title", category="")
        created_task = TaskOutput(id=1, title="Task Title", category="")
        self.mock_service.create_task.return_value = created_task

        client = self._create_test_app()
        response = client.post("/tasks/", json=task_input.model_dump())

        assert response.status_code == 201
        data = response.json()
        assert data["category"] == ""
        self.mock_service.create_task.assert_called_once()

    def test_get_task_by_id_success(self):
        """Test successful get task by ID endpoint"""
        task_id = 1
        task = TaskOutput(id=task_id, title="Test Task", category="Testing")
        self.mock_service.get_task_by_id.return_value = task

        client = self._create_test_app()
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task"
        assert data["category"] == "Testing"
        self.mock_service.get_task_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_not_found(self):
        """Test get task by ID when task doesn't exist"""
        task_id = 999
        self.mock_service.get_task_by_id.return_value = None

        client = self._create_test_app()
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Task not found"
        self.mock_service.get_task_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_with_zero_id(self):
        """Test get task by ID with zero ID"""
        task_id = 0
        self.mock_service.get_task_by_id.return_value = None

        client = self._create_test_app()
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Task not found"
        self.mock_service.get_task_by_id.assert_called_once_with(task_id)

    def test_get_task_by_id_with_negative_id(self):
        """Test get task by ID with negative ID"""
        task_id = -1
        self.mock_service.get_task_by_id.return_value = None

        client = self._create_test_app()
        response = client.get(f"/tasks/{task_id}")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Task not found"
        self.mock_service.get_task_by_id.assert_called_once_with(task_id)

    def test_update_task_success(self):
        """Test successful task update endpoint"""
        task_id = 1
        task_input = TaskInput(title="Updated Task", category="Updated Category")
        updated_task = TaskOutput(
            id=task_id, title="Updated Task", category="Updated Category"
        )
        self.mock_service.update_task.return_value = updated_task

        client = self._create_test_app()
        response = client.put(f"/tasks/{task_id}", json=task_input.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Updated Task"
        assert data["category"] == "Updated Category"
        self.mock_service.update_task.assert_called_once()

    def test_update_task_not_found(self):
        """Test update task when task doesn't exist"""
        task_id = 999
        task_input = TaskInput(title="Updated Task", category="Updated Category")
        self.mock_service.update_task.return_value = None

        client = self._create_test_app()
        response = client.put(f"/tasks/{task_id}", json=task_input.model_dump())

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Task not found"
        self.mock_service.update_task.assert_called_once()

    def test_update_task_with_empty_data(self):
        """Test update task with empty title and category"""
        task_id = 1
        task_input = TaskInput(title="", category="")
        updated_task = TaskOutput(id=task_id, title="", category="")
        self.mock_service.update_task.return_value = updated_task

        client = self._create_test_app()
        response = client.put(f"/tasks/{task_id}", json=task_input.model_dump())

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == ""
        assert data["category"] == ""
        self.mock_service.update_task.assert_called_once()

    def test_delete_task_success(self):
        """Test successful task deletion endpoint"""
        task_id = 1
        delete_response = DeleteTaskResponse(
            message=f"Task {task_id} eliminada correctamente"
        )
        self.mock_service.delete_task.return_value = delete_response

        client = self._create_test_app()
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Task {task_id} eliminada correctamente"
        self.mock_service.delete_task.assert_called_once_with(task_id)

    def test_delete_task_not_found(self):
        """Test delete task when task doesn't exist"""
        task_id = 999
        delete_response = DeleteTaskResponse(message=f"Task {task_id} no encontrada")
        self.mock_service.delete_task.return_value = delete_response

        client = self._create_test_app()
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Task {task_id} no encontrada"
        self.mock_service.delete_task.assert_called_once_with(task_id)

    def test_delete_task_with_zero_id(self):
        """Test delete task with zero ID"""
        task_id = 0
        delete_response = DeleteTaskResponse(message=f"Task {task_id} no encontrada")
        self.mock_service.delete_task.return_value = delete_response

        client = self._create_test_app()
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Task {task_id} no encontrada"
        self.mock_service.delete_task.assert_called_once_with(task_id)

    def test_delete_task_with_negative_id(self):
        """Test delete task with negative ID"""
        task_id = -1
        delete_response = DeleteTaskResponse(message=f"Task {task_id} no encontrada")
        self.mock_service.delete_task.return_value = delete_response

        client = self._create_test_app()
        response = client.delete(f"/tasks/{task_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Task {task_id} no encontrada"
        self.mock_service.delete_task.assert_called_once_with(task_id)


class TestTaskControllerEdgeCases:
    """Edge cases and error scenarios for TaskController"""

    def setup_method(self):
        """Setup test fixtures"""
        self.mock_service = Mock(spec=TaskService)
        self.mock_service.create_task = AsyncMock()
        self.mock_service.get_all_tasks = AsyncMock()
        self.mock_service.get_task_by_id = AsyncMock()
        self.mock_service.update_task = AsyncMock()
        self.mock_service.delete_task = AsyncMock()

    def _create_test_app(self):
        """Helper method to create test app with dependency override"""
        app = FastAPI()
        app.include_router(router)
        app.dependency_overrides[get_task_service] = lambda: self.mock_service
        return TestClient(app)

    def test_invalid_json_payload(self):
        """Test controller with invalid JSON payload"""
        client = self._create_test_app()
        response = client.post("/tasks/", json={"invalid": "data"})

        assert response.status_code == 422  # Validation error

    def test_missing_required_fields(self):
        """Test controller with missing required fields"""
        client = self._create_test_app()
        response = client.post("/tasks/", json={"title": "Only title"})

        assert response.status_code == 422  # Validation error

    def test_service_exception_handling(self):
        """Test controller handles service exceptions gracefully"""
        self.mock_service.get_all_tasks.side_effect = Exception("Service error")

        client = self._create_test_app()

        response = client.get("/tasks/")

        assert response.status_code == 500
        assert response.json()["detail"] == "Internal server error"
