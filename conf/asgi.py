from contextlib import asynccontextmanager

from fastapi import FastAPI

from conf import settings
from middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from shared.connection import conn

from .routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    conn.init()
    await conn.ping()
    yield
    await conn.close()


def get_asgi_application() -> FastAPI:
    application = FastAPI(debug=settings.DEBUG, title=settings.APP_TITLE, lifespan=lifespan)

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    [application.include_router(router=router, prefix="/api") for router in routers]

    return application


app = get_asgi_application()
