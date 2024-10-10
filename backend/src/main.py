import time

import fastapi
import uvicorn
from cassandra.cqlengine import management
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router as api_endpoint_router

# from src.config.events import (
#     execute_backend_server_event_handler,
#     terminate_backend_server_event_handler,
# )
from src.config.manager import settings
from src.models.db.models import Message, User
from src.repository.cache import cache
from src.repository.database import database


def initialize_backend_application() -> fastapi.FastAPI:
    app = fastapi.FastAPI(**settings.set_backend_app_attributes)  # type: ignore

    async def startup_event():
        """Startup event handler to initialize connections."""
        # Initialize Redis connection
        await cache.initialize()

        # Initialize Cassandra connection
        database.connect()

        management.sync_table(User)
        management.sync_table(Message)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    app.add_event_handler("startup", startup_event)
    # app.add_event_handler(
    #     "shutdown",
    #     terminate_backend_server_event_handler(backend_app=app),
    # )

    app.include_router(router=api_endpoint_router, prefix=settings.API_PREFIX)

    return app


backend_app: fastapi.FastAPI = initialize_backend_application()

if __name__ == "__main__":
    uvicorn.run(
        app="main:backend_app",
        host=settings.BACKEND_SERVER_HOST,
        port=settings.BACKEND_SERVER_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOGGING_LEVEL,
    )

# uvicorn src.main:backend_app --host 0.0.0.0 --port 8000 --reload
