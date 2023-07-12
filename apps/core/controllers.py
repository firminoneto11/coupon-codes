from traceback import format_exc
from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from shared.connection import make_db_session
from shared.logger import logger

from .exceptions import AlreadyRegisteredException
from .repositories import CouponRepository
from .schemas import BaseCouponSchema, CouponSchema
from .utils import is_redeemable

CommonDep = Annotated[AsyncSession, Depends(make_db_session)]


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


async def consume_coupon(db_session: CommonDep, coupon_id: int) -> dict:
    repo = CouponRepository(db_session=db_session)

    if (coupon := await repo.get_by_id(coupon_id)) is None:
        raise HTTPException(status_code=404, detail=f"Coupon of id {coupon_id} not found")

    if not (await is_redeemable(coupon=coupon)):
        raise HTTPException(status_code=404, detail=f"Coupon of id {coupon_id} is not redeemable")
