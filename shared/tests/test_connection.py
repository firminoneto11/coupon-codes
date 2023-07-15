from unittest.mock import AsyncMock, MagicMock

from pytest import raises

from shared.connection import DBConnectionHandler


async def test_connection_handler() -> None:
    local_conn = DBConnectionHandler()
    mock_session = MagicMock()
    mock_session.close = AsyncMock()

    with raises(ValueError) as exc_info:
        local_conn.engine

    assert str(exc_info.value) == "Engine is None. Can not proceed."

    with raises(ValueError) as exc_info:
        local_conn.make_session

    assert str(exc_info.value) == "Session maker is None. Can not proceed."

    local_conn.init(sqlite=True)
    local_conn._sessions_tracker.add(mock_session)
    await local_conn.close()

    assert mock_session.close.call_count == 1
    assert mock_session.close.await_count == 1
