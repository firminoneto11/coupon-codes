from math import floor

from apps.core.models import Coupons
from shared.utils import utcnow


def test_coupons() -> None:
    current_timestamp = utcnow()
    expected_value = floor(current_timestamp.timestamp())
    coupon = Coupons(expiration_date=current_timestamp)

    assert coupon.expiration_date_as_unix == expected_value
    coupon.prepare_to_export()
    assert coupon.expiration_date == expected_value
