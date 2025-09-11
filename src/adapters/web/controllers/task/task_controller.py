from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from src.schemas.schemas import TaskInput, TaskOutput, DeleteTaskResponse
from src.adapters.services.task.task_service import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


def get_task_service() -> TaskService:
    """Dependency to get task service instance"""

    raise HTTPException(status_code=500, detail="Service not configured")


@router.get("/", response_model=List[TaskOutput], status_code=status.HTTP_200_OK)
async def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks"""
    tasks = await service.get_all_tasks()
    return tasks


@router.post("/", response_model=TaskOutput, status_code=status.HTTP_201_CREATED)
async def create_task(task_input: TaskInput, service: TaskService = Depends(get_task_service)):
    """Create a new task"""
    task = await service.create_task(task_input)
    return task


@router.get("/{task_id}", response_model=TaskOutput, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, service: TaskService = Depends(get_task_service)):
    """Get task by id"""
    task = await service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.put("/{task_id}", response_model=TaskOutput, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task_input: TaskInput, service: TaskService = Depends(get_task_service)):
    """Update a task"""
    task = await service.update_task(task_id, task_input)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete(
    "/{task_id}", response_model=DeleteTaskResponse, status_code=status.HTTP_200_OK
)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Delete a task"""
    result = await service.delete_task(task_id)
    return result
