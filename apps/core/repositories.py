from dataclasses import dataclass

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from .exceptions import AlreadyRegisteredException
from .models import Coupons, Redemptions


@dataclass
class CouponRepository:
    db_session: AsyncSession

    async def get_by_code(self, coupon_code: str) -> Coupons | None:
        async with self.db_session as ses:
            try:
                return await ses.scalar(select(Coupons).filter(Coupons.code == coupon_code))
            except NoResultFound:
                return

    async def create(self, /, **kwargs) -> Coupons:
        coupon = Coupons(**kwargs)

        if await self.is_already_registered(code=coupon.code):
            raise AlreadyRegisteredException()

        async with self.db_session as ses:
            try:
                ses.add(coupon)
                await ses.commit()
                await ses.refresh(coupon)
                return coupon
            except Exception as exc:
                await ses.rollback()
                raise exc

    async def is_already_registered(self, code: str) -> bool:
        stmt = select(Coupons).filter(Coupons.code == code)
        async with self.db_session as ses:
            try:
                if (await ses.execute(stmt)).scalar():
                    return True
                return False
            except NoResultFound:
                return False


@dataclass
class RedemptionsRepository:
    db_session: AsyncSession

    async def create(self, /, **kwargs) -> Redemptions:
        redemption = Redemptions(**kwargs)
        async with self.db_session as ses:
            try:
                ses.add(redemption)
                await ses.commit()
                return await ses.scalar(
                    (
                        select(Redemptions)
                        .where(Redemptions.id == redemption.id)
                        .options(joinedload(Redemptions.coupon))
                    )
                )
            except Exception as exc:
                await ses.rollback()
                raise exc

    async def count_redemptions(self, coupon_id: int) -> int:
        stmt = (
            select(func.count()).select_from(Redemptions).filter(Redemptions.coupon_id == coupon_id)
        )
        async with self.db_session as ses:
            try:
                result = await ses.scalar(stmt)
                return result or 0
            except NoResultFound:
                return 0
