from dataclasses import dataclass

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .exceptions import AlreadyRegisteredException
from .models import Coupons, Redemptions


@dataclass
class CouponRepository:
    db_session: AsyncSession

    async def get_by_id(self, id: int) -> Coupons | None:
        async with self.db_session as ses:
            return await ses.get(Coupons, id)

    async def create(self, /, **kwargs) -> Coupons:
        coupon = Coupons(**kwargs)

        if await self.is_already_registered(code=coupon.code):
            raise AlreadyRegisteredException()

        async with self.db_session as ses:
            ses.add(coupon)
            await ses.commit()
            await ses.refresh(coupon)
            return coupon

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

    async def get_by_id(self, id: int) -> Redemptions | None:
        async with self.db_session as ses:
            return await ses.get(Redemptions, id)

    async def create(self, /, **kwargs) -> Redemptions:
        redemption = Redemptions(**kwargs)
        async with self.db_session as ses:
            ses.add(redemption)
            await ses.commit()
            await ses.refresh(redemption)
            return redemption
