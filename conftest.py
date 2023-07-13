from asyncio import new_event_loop, set_event_loop

from httpx import AsyncClient
from pytest import fixture
from uvloop import install

from config.asgi import get_asgi_application


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
    async with AsyncClient(app=get_asgi_application(), base_url="http://test") as client:
        yield client
