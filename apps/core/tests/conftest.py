from pytest import fixture

from shared.utils import unix_timestamp


@fixture
def create_coupon_data() -> dict:
    return {
        "code": "coupon1",
        "type": "PERCENTAGE",
        "expiration_date": unix_timestamp() + 300_000,
        "max_redemption_quota": 3,
        "minimum_purchase_amount": 100.00,
        "discount_amount": 10,
        "first_purchase_only": False,
        "available_for_general_public": False,
    }


@fixture
def consume_coupon_data() -> dict:
    return {
        "total_purchase_amount": 1000,
        "is_first_purchase": True,
    }
