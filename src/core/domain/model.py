from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    """Domain model for Task"""

    id: Optional[int] = Field(default=None)
    title: str
    category: str
    created_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default=None)

    class Config:
        populate_by_name = True
