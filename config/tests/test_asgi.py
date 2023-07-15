from unittest.mock import AsyncMock, MagicMock, patch

from config.asgi import lifespan


async def test_lifespan() -> None:
    mock = MagicMock()
    mock.init = MagicMock()
    mock.close = AsyncMock()

    with patch(target="config.asgi.conn", new=mock):
        async with lifespan(app=None):
            pass

    assert mock.init.call_count == 1
    assert mock.close.call_count == 1
    assert mock.close.await_count == 1
