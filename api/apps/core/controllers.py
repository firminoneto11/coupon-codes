from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shared.connection import make_db_session

from .repositories import CouponRepository
from .schemas import BaseCouponSchema, CouponSchema


async def register_coupon(
    data: BaseCouponSchema, db_session: Annotated[AsyncSession, Depends(make_db_session)]
) -> CouponSchema:
    repo = CouponRepository(db_session=db_session)
    coupon = await repo.create(**data.model_dump())
    return coupon


async def consume_coupon(coupon_id: int):
    pass
