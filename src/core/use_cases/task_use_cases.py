from typing import List, Optional
from src.core.domain.model import Task
from src.core.platform.appcontext.appcontext import Context


class CreateTaskUseCase:
    """Use case for creating a new task"""

    def __init__(self, context: Context):
        self.context = context

    def execute(self, title: str, category: str) -> Task:
        """Create a new task"""
        task = Task(title=title, category=category)
        return self.context.repositories.task.create(task)


class GetAllTasksUseCase:
    """Use case for getting all tasks"""

    def __init__(self, context: Context):
        self.context = context

    def execute(self) -> List[Task]:
        """Get all tasks"""

        return self.context.repositories.task.find_all()


class GetTaskByIdUseCase:
    """Use case for getting a task by id"""

    def __init__(self, context: Context):
        self.context = context

    def execute(self, task_id: int) -> Optional[Task]:
        """Get task by id"""

        return self.context.repositories.task.find_by_id(task_id)


class UpdateTaskUseCase:
    """Use case for updating a task"""

    def __init__(self, context: Context):
        self.context = context

    def execute(self, task_id: int, title: str, category: str) -> Optional[Task]:
        """Update a task"""
        task = Task(title=title, category=category)
        return self.context.repositories.task.update(task_id, task)


class DeleteTaskUseCase:
    """Use case for deleting a task"""

    def __init__(self, context: Context):
        self.context = context

    def execute(self, task_id: int) -> bool:
        """Delete a task"""
        return self.context.repositories.task.delete(task_id)
