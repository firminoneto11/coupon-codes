from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, field_validator

from shared.utils import unix_timestamp

from .enums import DiscountTypesEnum


class BaseCouponSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    type: Literal[
        DiscountTypesEnum.PERCENTAGE,
        DiscountTypesEnum.FIXED_AMOUNT_FIRST_PURCHASE,
        DiscountTypesEnum.FIXED_AMOUNT_GENERAL_PUBLIC,
    ]

    expiration_date: int

    max_redemption_quota: int
    minimum_purchase_amount: float
    discount_amount: float

    first_purchase_only: bool
    available_for_general_public: bool

    @staticmethod
    def convert_into_datetime(expiration_date: int) -> datetime:
        try:
            return datetime.utcfromtimestamp(expiration_date).replace(tzinfo=timezone.utc)
        except:
            raise ValueError(f"Invalid unix timestamp: {expiration_date!r}")

    @field_validator("expiration_date")
    def validate_expiration_date(cls, expiration_date: int) -> int:
        if unix_timestamp() >= expiration_date:
            raise ValueError("The unix timestamp provided is set to a past date!")
        return expiration_date

    @field_validator("first_purchase_only")
    def validate_first_purchase_only(cls, first_purchase_only: bool, values: dict):
        if (
            values["type"] == DiscountTypesEnum.FIXED_AMOUNT_FIRST_PURCHASE
            and not first_purchase_only
        ):
            raise ValueError(
                f"When the coupon's type is {values['type']} the value for the"
                f"'first_purchase_only' field has to be true"
            )

        return first_purchase_only

    @field_validator("available_for_general_public")
    def validate_available_for_general_public(
        cls, available_for_general_public: bool, values: dict
    ) -> bool:
        if (
            values["type"] == DiscountTypesEnum.FIXED_AMOUNT_GENERAL_PUBLIC
            and not available_for_general_public
        ):
            raise ValueError(
                f"When the coupon's type is {values['type']} the value for the"
                f"'available_for_general_public' field has to be true"
            )

        return available_for_general_public

    def to_dict(self) -> dict:
        data = self.model_dump()
        data["expiration_date"] = self.convert_into_datetime(self.expiration_date)
        return data


class CouponSchema(BaseCouponSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class RedemptionSchemaIn(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    total_purchase_amount: float
    is_first_purchase: bool


class RedemptionSchemaOut(RedemptionSchemaIn):
    id: int
    created_at: datetime
    updated_at: datetime
    total_amount_with_discount: float
    coupon: CouponSchema
