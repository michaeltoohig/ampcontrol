from fastapi import FastAPI

from app.api import root
from app.api.api_v1.api import api_router
from app.core.config import settings


def create_api():
    app = FastAPI()

    app.include_router(root.router)
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
