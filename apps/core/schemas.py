from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, validator

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

    general_public: bool
    first_purchase: bool

    @staticmethod
    def convert_into_datetime(expiration_date: int) -> datetime:
        try:
            return datetime.utcfromtimestamp(expiration_date).replace(tzinfo=timezone.utc)
        except:
            raise ValueError(f"Invalid unix timestamp: {expiration_date!r}")

    @validator("expiration_date")
    def validate_expiration_date(cls, expiration_date: int) -> int:
        if unix_timestamp() >= expiration_date:
            raise ValueError("The unix timestamp provided is set to a past date!")
        return expiration_date

    def to_dict(self) -> dict:
        data = self.model_dump()
        data["expiration_date"] = self.convert_into_datetime(self.expiration_date)
        return data


class CouponSchema(BaseCouponSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class RedemptionSchema(BaseModel):
    total_purchase_amount: float
    is_first_purchase: bool
