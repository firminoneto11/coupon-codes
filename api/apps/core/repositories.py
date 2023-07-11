from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from .models import Coupons, Redemptions


@dataclass
class CouponRepository:
    db_session: AsyncSession

    async def get_by_id(self, id: int) -> Coupons | None:
        async with self.db_session as ses:
            return await ses.get(Coupons, id)

    async def create(self, /, **kwargs) -> Coupons:
        coupon = Coupons(**kwargs)
        async with self.db_session as ses:
            ses.add(coupon)
            await ses.commit()
            await ses.refresh(coupon)
            return coupon


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
