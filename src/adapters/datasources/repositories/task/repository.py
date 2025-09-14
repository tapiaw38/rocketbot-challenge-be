from typing import List, Optional
from datetime import datetime
from src.core.domain.model import Task
from src.adapters.datasources.repositories.task.repository_interface import (
    TaskRepositoryInterface,
)


class InMemoryTaskRepository(TaskRepositoryInterface):
    """In-memory implementation of Task repository"""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1

    def create(self, task: Task) -> Task:
        """Create a new task"""
        task.id = self._next_id
        now = datetime.now()
        task.created_at = now
        task.updated_at = now
        self._tasks.append(task)
        self._next_id += 1
        return task

    def find_all(self) -> List[Task]:
        """Find all tasks"""
        return self._tasks.copy()

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by id"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task_id: int, task: Task) -> Optional[Task]:
        """Update task by id"""
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == task_id:
                task.id = task_id
                task.created_at = existing_task.created_at
                task.updated_at = datetime.now()
                self._tasks[i] = task
                return task
        return None

    def delete(self, task_id: int) -> bool:
        """Delete task by id"""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False
