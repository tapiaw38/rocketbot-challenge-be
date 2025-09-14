from fastapi import APIRouter, status, HTTPException, Depends
from typing import List
from src.schemas.schemas import TaskInput, TaskOutput, DeleteTaskResponse
from src.adapters.services.task.task_service import TaskService
from src.core.platform.logging import Logger


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

logger = Logger("task_controller")


def get_task_service() -> TaskService:
    """Dependency to get task service instance"""
    logger.error("Service not configured - dependency injection failed")
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Service not configured",
    )


@router.get("/", response_model=List[TaskOutput], status_code=status.HTTP_200_OK)
async def get_all_tasks(service: TaskService = Depends(get_task_service)):
    """Get all tasks"""
    try:
        logger.info("GET /tasks - Retrieving all tasks")
        tasks = await service.get_all_tasks()
        logger.info(f"GET /tasks - Successfully retrieved {len(tasks)} tasks")
        return tasks
    except Exception as e:
        logger.log_exception("GET /tasks - Error retrieving tasks", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post("/", response_model=TaskOutput, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_input: TaskInput, service: TaskService = Depends(get_task_service)
):
    """Create a new task"""
    try:
        logger.info(f"POST /tasks - Creating task: {task_input.title}")
        task = await service.create_task(task_input)
        logger.info(f"POST /tasks - Task created successfully with ID: {task.id}")
        return task
    except Exception as e:
        logger.log_exception("POST /tasks - Error creating task", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{task_id}", response_model=TaskOutput, status_code=status.HTTP_200_OK)
async def get_task_by_id(
    task_id: int, service: TaskService = Depends(get_task_service)
):
    """Get task by id"""
    try:
        logger.info(f"GET /tasks/{task_id} - Retrieving task")
        task = await service.get_task_by_id(task_id)
        if not task:
            logger.warning(f"GET /tasks/{task_id} - Task not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        logger.info(f"GET /tasks/{task_id} - Task found: {task.title}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.log_exception(f"GET /tasks/{task_id} - Error retrieving task", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.put("/{task_id}", response_model=TaskOutput, status_code=status.HTTP_200_OK)
async def update_task(
    task_id: int,
    task_input: TaskInput,
    service: TaskService = Depends(get_task_service),
):
    """Update a task"""
    try:
        logger.info(f"PUT /tasks/{task_id} - Updating task")
        task = await service.update_task(task_id, task_input)
        if not task:
            logger.warning(f"PUT /tasks/{task_id} - Task not found for update")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        logger.info(f"PUT /tasks/{task_id} - Task updated successfully: {task.title}")
        return task
    except HTTPException:
        raise
    except Exception as e:
        logger.log_exception(f"PUT /tasks/{task_id} - Error updating task", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.delete(
    "/{task_id}", response_model=DeleteTaskResponse, status_code=status.HTTP_200_OK
)
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    """Delete a task"""
    try:
        logger.info(f"DELETE /tasks/{task_id} - Deleting task")
        result = await service.delete_task(task_id)
        logger.info(f"DELETE /tasks/{task_id} - Task deletion completed")
        return result
    except Exception as e:
        logger.log_exception(f"DELETE /tasks/{task_id} - Error deleting task", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
