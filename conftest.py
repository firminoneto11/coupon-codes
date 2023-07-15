from asyncio import new_event_loop, set_event_loop
from unittest.mock import AsyncMock, MagicMock, patch

from httpx import AsyncClient
from pytest import fixture
from uvloop import install

from config import settings
from config.asgi import get_asgi_application
from shared.connection import conn


@fixture(scope="session", autouse=True)
def event_loop():
    """Overrides pytest's default function scoped event loop"""

    install()

    set_event_loop(loop=(loop := new_event_loop()))

    yield loop

    if loop.is_running():
        loop.stop()

    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.run_until_complete(loop.shutdown_default_executor())

    loop.close()


@fixture(scope="session")
async def client():
    mock = MagicMock()
    mock.init = MagicMock()
    mock.close = AsyncMock()
    with patch(target="config.asgi.conn", new=mock):
        async with AsyncClient(app=get_asgi_application(), base_url="http://test") as client:
            yield client


@fixture(scope="session", autouse=True)
async def connection():
    for imp in [f"from apps.{app} import models" for app in settings.APPS]:
        exec(imp)

    conn.init(sqlite=True)
    await conn.execute_ddl()

    try:
        yield conn
    finally:
        await conn.close()
