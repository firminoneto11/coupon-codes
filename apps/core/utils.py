from fastapi import HTTPException

from shared.utils import unix_timestamp

from .enums import DiscountTypesEnum
from .models import Coupons
from .repositories import RedemptionsRepository
from .schemas import RedemptionSchema


async def is_redeemable(
    coupon: Coupons, repo: RedemptionsRepository, data: RedemptionSchema
) -> None:
    if unix_timestamp() >= coupon.expiration_date_as_unix:
        raise HTTPException(status_code=400, detail="Coupon has expired")

    if (await repo.count_redemptions(coupon_id=coupon.id)) > coupon.max_redemption_quota:
        raise HTTPException(status_code=400, detail="Coupon reached the maximum redemption quota")

    if data.total_purchase_amount < coupon.minimum_purchase_amount:
        raise HTTPException(
            status_code=400,
            detail=f"The minimum purchase amount for this coupon is ${coupon.minimum_purchase_amount}",
        )


async def redeem(coupon: Coupons, repo: RedemptionsRepository, data: RedemptionSchema) -> None:
    pass
