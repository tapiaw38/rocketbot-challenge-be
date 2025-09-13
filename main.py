from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from src.routes.routes_manager import RoutesManager
from src.core.platform.logging import Logger


logger = Logger("main")

app = FastAPI(
    title="RocketBot Challenge API",
    description="API for managing tasks - RocketBot Challenge",
    version="1.0.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """Redirect root path to API documentation"""
    logger.info("GET / - Redirecting to API documentation")
    return RedirectResponse(url="/docs")


@app.get("/health", include_in_schema=False)
async def health_check():
    """Health check endpoint"""
    logger.info("GET /health - Health check requested")
    return {"status": "healthy", "message": "RocketBot Challenge API is running"}


logger.info("Initializing routes...")
routes_manager = RoutesManager(app)
routes_manager.include_routes()
logger.info("Routes initialized successfully")


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting RocketBot Challenge API server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
