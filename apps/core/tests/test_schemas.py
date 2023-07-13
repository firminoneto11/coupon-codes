from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from pydantic import ValidationError
from pytest import raises

from apps.core.enums import DiscountTypesEnum
from apps.core.schemas import BaseCouponSchema


def test_base_coupon_schema_convert_into_datetime(create_coupon_data: dict) -> None:
    schema = BaseCouponSchema(**create_coupon_data)
    expected_dt = datetime.utcfromtimestamp(schema.expiration_date).replace(tzinfo=timezone.utc)
    expected_error_message = f"Invalid unix timestamp: {schema.expiration_date!r}"

    mock = MagicMock()
    mock.fromtimestamp = MagicMock(side_effect=ValueError())
    with patch(target="apps.core.schemas.datetime", new=mock):
        with raises(ValueError) as exc_info:
            schema.convert_into_datetime(schema.expiration_date)

    assert schema.convert_into_datetime(schema.expiration_date) == expected_dt
    assert str(exc_info.value) == expected_error_message


def test_base_coupon_schema_validate_expiration_date(create_coupon_data: dict) -> None:
    create_coupon_data["expiration_date"] = 123

    expected_error_message = "Value error, The unix timestamp provided is set to a past date!"

    with raises(ValidationError) as exc_info:
        BaseCouponSchema(**create_coupon_data)

    assert exc_info.value.errors()[0]["msg"] == expected_error_message


def test_base_coupon_schema_to_dict(create_coupon_data: dict) -> None:
    schema = BaseCouponSchema(**create_coupon_data)
    create_coupon_data["expiration_date"] = schema.convert_into_datetime(schema.expiration_date)

    assert schema.to_dict() == create_coupon_data


def test_base_coupon_schema_first_purchase_only(create_coupon_data: dict) -> None:
    create_coupon_data["type"] = DiscountTypesEnum.FIXED_AMOUNT_FIRST_PURCHASE

    expected_error_message = (
        f"Value error, When the coupon's type is {create_coupon_data['type']} the value for the"
        f"'first_purchase_only' field has to be true"
    )

    with raises(ValidationError) as exc_info:
        BaseCouponSchema(**create_coupon_data)

    assert exc_info.value.errors()[0]["msg"] == expected_error_message


def test_base_coupon_schema_available_for_general_public(create_coupon_data: dict) -> None:
    create_coupon_data["type"] = DiscountTypesEnum.FIXED_AMOUNT_GENERAL_PUBLIC

    expected_error_message = (
        f"Value error, When the coupon's type is {create_coupon_data['type']} the value for the"
        f"'available_for_general_public' field has to be true"
    )

    with raises(ValidationError) as exc_info:
        BaseCouponSchema(**create_coupon_data)

    assert exc_info.value.errors()[0]["msg"] == expected_error_message
