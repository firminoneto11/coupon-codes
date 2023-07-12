from fastapi import HTTPException

from shared.utils import unix_timestamp

from .enums import DiscountTypesEnum
from .models import Coupons, Redemptions
from .repositories import RedemptionsRepository
from .schemas import RedemptionSchemaIn


async def is_redeemable(
    coupon: Coupons, repo: RedemptionsRepository, data: RedemptionSchemaIn
) -> None:
    if unix_timestamp() >= coupon.expiration_date_as_unix:
        raise HTTPException(status_code=400, detail="Coupon has expired")

    if (await repo.count_redemptions(coupon_id=coupon.id)) >= coupon.max_redemption_quota:
        raise HTTPException(status_code=400, detail="Coupon reached the maximum redemption quota")

    if data.total_purchase_amount < coupon.minimum_purchase_amount:
        raise HTTPException(
            status_code=400,
            detail=f"The minimum purchase amount for this coupon is ${coupon.minimum_purchase_amount}",
        )

    if (coupon.first_purchase_only) and (not data.is_first_purchase):
        raise HTTPException(
            status_code=400, detail="This coupon is available for the first purchase only"
        )


async def redeem(
    coupon: Coupons, repo: RedemptionsRepository, data: RedemptionSchemaIn
) -> Redemptions:
    match coupon.type:
        case DiscountTypesEnum.PERCENTAGE:
            discount = data.total_purchase_amount * (coupon.discount_amount / 100)
            total_amount_with_discount = data.total_purchase_amount - discount
        case _:
            total_amount_with_discount = data.total_purchase_amount - coupon.discount_amount

    redeemed_coupon = await repo.create(
        coupon_id=coupon.id,
        total_purchase_amount=data.total_purchase_amount,
        total_amount_with_discount=total_amount_with_discount,
        is_first_purchase=data.is_first_purchase,
    )

    redeemed_coupon.coupon.prepare_to_export()

    return redeemed_coupon
