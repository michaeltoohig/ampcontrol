from fastapi import FastAPI

from app.api import hello
from app.api.api_v1.api import api_router
from app.core.config import settings


def create_api():
    app = FastAPI()

    app.include_router(hello.router)  # TODO remove after setting up our tests
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
