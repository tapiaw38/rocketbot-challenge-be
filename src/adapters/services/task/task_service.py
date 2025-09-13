from typing import List, Optional
from src.core.use_cases.use_cases import Usecases
from src.schemas.schemas import TaskInput, TaskOutput, DeleteTaskResponse
from src.core.platform.logging import Logger


class TaskService:
    """Service for task operations"""

    def __init__(self, usecases: Usecases, logger: Optional[Logger] = None):
        self.usecases = usecases
        self.logger = logger or Logger("task_service")

    async def create_task(self, task_input: TaskInput) -> TaskOutput:
        """Create a new task"""
        try:
            self.logger.info(f"Creating task: {task_input.title}")
            task = self.usecases.task.create_usecase.execute(
                title=task_input.title, category=task_input.category
            )
            self.logger.info(f"Task created successfully with ID: {task.id}")
            return TaskOutput.from_task(task)
        except Exception as e:
            self.logger.log_exception("Error creating task", e)
            raise

    async def get_all_tasks(self) -> List[TaskOutput]:
        """Get all tasks"""
        try:
            self.logger.info("Retrieving all tasks")
            tasks = self.usecases.task.get_all_usecase.execute()
            self.logger.info(f"Retrieved {len(tasks)} tasks")
            return [TaskOutput.from_task(task) for task in tasks]
        except Exception as e:
            self.logger.log_exception("Error retrieving all tasks", e)
            raise

    async def get_task_by_id(self, task_id: int) -> Optional[TaskOutput]:
        """Get task by id"""
        try:
            self.logger.info(f"Retrieving task with ID: {task_id}")
            task = self.usecases.task.get_by_id_usecase.execute(task_id)
            if task:
                self.logger.info(f"Task found: {task.title}")
                return TaskOutput.from_task(task)
            else:
                self.logger.warning(f"Task not found with ID: {task_id}")
                return None
        except Exception as e:
            self.logger.log_exception(f"Error retrieving task with ID: {task_id}", e)
            raise

    async def update_task(
        self, task_id: int, task_input: TaskInput
    ) -> Optional[TaskOutput]:
        """Update a task"""
        try:
            self.logger.info(f"Updating task with ID: {task_id}")
            task = self.usecases.task.update_usecase.execute(
                task_id=task_id, title=task_input.title, category=task_input.category
            )
            if task:
                self.logger.info(f"Task updated successfully: {task.title}")
                return TaskOutput.from_task(task)
            else:
                self.logger.warning(f"Task not found for update with ID: {task_id}")
                return None
        except Exception as e:
            self.logger.log_exception(f"Error updating task with ID: {task_id}", e)
            raise

    async def delete_task(self, task_id: int) -> DeleteTaskResponse:
        """Delete a task"""
        try:
            self.logger.info(f"Deleting task with ID: {task_id}")
            success = self.usecases.task.delete_usecase.execute(task_id)
            if success:
                self.logger.info(f"Task deleted successfully with ID: {task_id}")
                return DeleteTaskResponse(message=f"Task {task_id} eliminada correctamente")
            else:
                self.logger.warning(f"Task not found for deletion with ID: {task_id}")
                return DeleteTaskResponse(message=f"Task {task_id} no encontrada")
        except Exception as e:
            self.logger.log_exception(f"Error deleting task with ID: {task_id}", e)
            raise
