from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from .enums import DiscountTypesEnum


class BaseCouponSchema(BaseModel):
    code: str
    type: Literal[
        DiscountTypesEnum.PERCENTAGE,
        DiscountTypesEnum.FIXED_AMOUNT_FIRST_PURCHASE,
        DiscountTypesEnum.FIXED_AMOUNT_GENERAL_PUBLIC,
    ]

    expiration_date: datetime

    max_redemption_quota: int
    minimum_purchase_amount: float
    discount_amount: float

    general_public: bool
    first_purchase: bool


class CouponSchema(BaseCouponSchema):
    id: int
