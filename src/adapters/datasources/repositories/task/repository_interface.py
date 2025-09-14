from abc import ABC, abstractmethod
from typing import List, Optional
from src.core.domain.model import Task


class TaskRepositoryInterface(ABC):
    """Interface for Task repository"""

    @abstractmethod
    def create(self, task: Task) -> Task:
        """Create a new task"""
        pass

    @abstractmethod
    def find_all(self) -> List[Task]:
        """Find all tasks"""
        pass

    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find task by id"""
        pass

    @abstractmethod
    def update(self, task_id: int, task: Task) -> Optional[Task]:
        """Update task by id"""
        pass


@abstractmethod
def delete(self, task_id: int) -> bool:
    """Delete task by id"""
    pass
