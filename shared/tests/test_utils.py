from datetime import datetime, timezone
from math import floor
from unittest.mock import MagicMock, patch

from shared.utils import unix_timestamp, utcnow


def test_utcnow() -> None:
    current_timestamp = datetime.now(tz=timezone.utc)

    mock_obj = MagicMock()
    mock_obj.now = MagicMock(return_value=current_timestamp)

    with patch(target="shared.utils.datetime", new=mock_obj):
        value = utcnow()

    assert value is current_timestamp


def test_unix_timestamp() -> None:
    current_timestamp = utcnow()

    with patch(target="shared.utils.utcnow", new=MagicMock(return_value=current_timestamp)):
        value = unix_timestamp()

    assert value == floor(current_timestamp.timestamp())
