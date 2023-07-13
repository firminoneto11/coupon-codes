from pytest import raises

from shared.connection import DBConnectionHandler


def test_connection_handler() -> None:
    local_conn = DBConnectionHandler()

    with raises(ValueError) as exc_info:
        local_conn.engine

    assert str(exc_info.value) == "Engine is None. Can not proceed."

    with raises(ValueError) as exc_info:
        local_conn.session_maker

    assert str(exc_info.value) == "Session maker is None. Can not proceed."
