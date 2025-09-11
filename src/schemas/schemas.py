from pydantic import BaseModel
from typing import Optional


class TaskInput(BaseModel):
    """Input schema for task creation and update"""

    title: str
    category: str


class TaskOutput(BaseModel):
    """Output schema for task responses"""

    id: int
    title: str
    category: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    @classmethod
    def from_task(cls, task) -> "TaskOutput":
        """Create TaskOutput from Task domain model"""
        return cls(
            id=task.id,
            title=task.title,
            category=task.category,
            created_at=task.created_at.isoformat() if task.created_at else None,
            updated_at=task.updated_at.isoformat() if task.updated_at else None,
        )


class DeleteTaskResponse(BaseModel):
    """Response schema for task deletion"""

    message: str
