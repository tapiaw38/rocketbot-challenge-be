from src.adapters.datasources.datasources import Datasources
from src.adapters.datasources.repositories.task.repository import \
    InMemoryTaskRepository


class Repositories:
    """Container for all repositories"""

    def __init__(self, task: InMemoryTaskRepository):
        self.task = task

    @staticmethod
    def create_repositories(datasources: Datasources):
        """Factory method to create repositories"""
        return Repositories(
            task=InMemoryTaskRepository(),
        )
