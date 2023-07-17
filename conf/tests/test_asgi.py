from unittest.mock import AsyncMock, MagicMock, patch

from conf.asgi import lifespan


async def test_lifespan() -> None:
    mock = MagicMock()
    mock.init = MagicMock()
    mock.ping = AsyncMock()
    mock.close = AsyncMock()

    with patch(target="conf.asgi.conn", new=mock):
        async with lifespan(app=None):
            pass

    assert mock.init.call_count == 1
    assert mock.ping.call_count == 1
    assert mock.ping.await_count == 1
    assert mock.close.call_count == 1
    assert mock.close.await_count == 1
