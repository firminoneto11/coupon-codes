from fastapi import FastAPI

from conf import settings
from shared.connection import database

from ..middleware import (
    allowed_hosts_middleware_configuration,
    cors_middleware_configuration,
)
from .routers import routers


async def startup() -> None:
    database.init(url=settings.ASYNCPG_URL)


async def shutdown() -> None:
    await database.close()


def get_asgi_application() -> FastAPI:
    application = FastAPI(debug=settings.DEBUG, title=settings.APP_TITLE)

    application.add_middleware(**allowed_hosts_middleware_configuration)
    application.add_middleware(**cors_middleware_configuration)

    application.on_event("startup")(startup)
    application.on_event("shutdown")(shutdown)

    [application.include_router(router=router, prefix="/api") for router in routers]

    return application


app = get_asgi_application()
