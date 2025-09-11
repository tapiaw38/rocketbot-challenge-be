from typing import List, Optional
from src.core.use_cases.use_cases import Usecases
from src.schemas.schemas import TaskInput, TaskOutput, DeleteTaskResponse


class TaskService:
    """Service for task operations"""

    def __init__(self, usecases: Usecases):
        self.usecases = usecases

    async def create_task(self, task_input: TaskInput) -> TaskOutput:
        """Create a new task"""
        task = self.usecases.task.create_usecase.execute(
            title=task_input.title, category=task_input.category
        )
        return TaskOutput.from_task(task)

    async def get_all_tasks(self) -> List[TaskOutput]:
        """Get all tasks"""
        tasks = self.usecases.task.get_all_usecase.execute()
        return [TaskOutput.from_task(task) for task in tasks]

    async def get_task_by_id(self, task_id: int) -> Optional[TaskOutput]:
        """Get task by id"""
        task = self.usecases.task.get_by_id_usecase.execute(task_id)
        if task:
            return TaskOutput.from_task(task)
        return None

    async def update_task(
        self, task_id: int, task_input: TaskInput
    ) -> Optional[TaskOutput]:
        """Update a task"""
        task = self.usecases.task.update_usecase.execute(
            task_id=task_id, title=task_input.title, category=task_input.category
        )
        if task:
            return TaskOutput.from_task(task)
        return None

    async def delete_task(self, task_id: int) -> DeleteTaskResponse:
        """Delete a task"""
        success = self.usecases.task.delete_usecase.execute(task_id)
        if success:
            return DeleteTaskResponse(message=f"Task {task_id} eliminada correctamente")
        return DeleteTaskResponse(message=f"Task {task_id} no encontrada")
