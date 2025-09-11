from fastapi import FastAPI
from src.adapters.web.controllers.task.task_controller import router as task_router, get_task_service
from src.adapters.services.task.task_service import TaskService
from src.core.use_cases.use_cases import create_usecases
from src.adapters.datasources.datasources import Datasources
from src.core.platform.appcontext.appcontext import new_factory


class RoutesManager:
    """Manager for API routes"""

    def __init__(self, app: FastAPI):
        self.app = app

    def include_routes(self):
        """Include all routes in the FastAPI app"""
        datasources = Datasources.create_datasources()
        context_factory = new_factory(datasources)
        usecases = create_usecases(context_factory)
        task_service = TaskService(usecases)

        # Override the dependency function to return our configured service
        self.app.dependency_overrides[get_task_service] = lambda: task_service

        self.app.include_router(task_router)
