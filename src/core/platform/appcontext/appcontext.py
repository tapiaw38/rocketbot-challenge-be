from typing import Callable, Optional
from src.adapters.datasources.datasources import Datasources
from src.adapters.datasources.repositories.repositories import Repositories
from src.core.platform.logging import Logger


class Context:
    """Application context holding repositories and other shared resources"""

    def __init__(
        self,
        repositories: Optional[Repositories] = None,
        logger: Optional[Logger] = None,
    ):
        self.repositories = repositories
        self.logger = logger or Logger("appcontext")


Option = Callable[[Context], None]
Factory = Callable[..., Context]


def new_factory(
    datasources: Datasources,
) -> Factory:
    """Create a new context factory"""

    def factory(*opts: Option) -> Context:
        context = Context(
            repositories=Repositories.create_repositories(datasources),
            logger=Logger("appcontext"),
        )
        for opt in opts:
            opt(context)
        return context

    return factory
