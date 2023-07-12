from datetime import datetime, timezone
from math import floor


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)


def unix_timestamp() -> int:
    return floor(utcnow().timestamp())
