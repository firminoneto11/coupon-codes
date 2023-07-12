from traceback import format_exc
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared.connection import make_db_session
from shared.logger import logger

from .exceptions import AlreadyRegisteredException
from .repositories import CouponRepository, RedemptionsRepository
from .schemas import (
    BaseCouponSchema,
    CouponSchema,
    RedemptionSchemaIn,
    RedemptionSchemaOut,
)
from .utils import is_redeemable, redeem

CommonDep = Annotated[AsyncSession, Depends(make_db_session)]


# TODO: Check the datetimes


async def register_coupon(db_session: CommonDep, data: BaseCouponSchema) -> CouponSchema:
    repo = CouponRepository(db_session=db_session)

    try:
        coupon = await repo.create(**data.to_dict())
        coupon.prepare_to_export()
        return coupon
    except AlreadyRegisteredException:
        raise HTTPException(
            status_code=400, detail="The code provided is registered in the database already"
        )
    except:
        await logger.error(format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def consume_coupon(
    db_session: CommonDep, data: RedemptionSchemaIn, coupon_code: str
) -> RedemptionSchemaOut:
    coupon_repo = CouponRepository(db_session=db_session)
    redemption_repo = RedemptionsRepository(db_session=db_session)

    if (coupon := await coupon_repo.get_by_code(coupon_code)) is None:
        raise HTTPException(status_code=404, detail=f"Coupon {coupon_code!r} not found")

    await is_redeemable(coupon=coupon, repo=redemption_repo, data=data)

    return await redeem(coupon=coupon, repo=redemption_repo, data=data)
