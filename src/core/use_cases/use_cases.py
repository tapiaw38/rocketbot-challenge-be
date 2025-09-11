from dataclasses import dataclass
from src.core.platform.appcontext.appcontext import Factory
from src.core.use_cases.task_use_cases import (
    CreateTaskUseCase,
    GetAllTasksUseCase,
    GetTaskByIdUseCase,
    UpdateTaskUseCase,
    DeleteTaskUseCase,
)


@dataclass
class Task:
    """Container for task-related use cases"""

    create_usecase: CreateTaskUseCase
    get_all_usecase: GetAllTasksUseCase
    get_by_id_usecase: GetTaskByIdUseCase
    update_usecase: UpdateTaskUseCase
    delete_usecase: DeleteTaskUseCase


@dataclass
class Usecases:
    """Container for all use cases"""

    task: Task


def create_usecases(context_factory: Factory) -> Usecases:
    """Create all use cases with the given context factory"""
    # Create a single shared context for all use cases

    context_factory = context_factory()
    return Usecases(
        task=Task(
            create_usecase=CreateTaskUseCase(context_factory),
            get_all_usecase=GetAllTasksUseCase(context_factory),
            get_by_id_usecase=GetTaskByIdUseCase(context_factory),
            update_usecase=UpdateTaskUseCase(context_factory),
            delete_usecase=DeleteTaskUseCase(context_factory),
        ),
    )
