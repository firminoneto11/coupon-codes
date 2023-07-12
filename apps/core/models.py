from datetime import datetime
from math import floor
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from shared.models import TimeStampedBaseModel

from .enums import DiscountTypesEnum


class Redemptions(TimeStampedBaseModel):
    if TYPE_CHECKING:
        coupon: "Coupons"

    __tablename__ = "redemptions"

    coupon_id: int = sa.Column(sa.BigInteger, sa.ForeignKey("coupons.id"), nullable=False)
    total_purchase_amount: float = sa.Column(sa.Double(precision=2), nullable=False)
    total_amount_with_discount: float = sa.Column(sa.Double(precision=2), nullable=False)
    is_first_purchase: bool = sa.Column(sa.Boolean, nullable=False)


class Coupons(TimeStampedBaseModel):
    __tablename__ = "coupons"

    code: str = sa.Column(sa.String(300), unique=True, nullable=False)
    type: str = sa.Column(sa.Enum(DiscountTypesEnum), nullable=False, name="type_enum")

    expiration_date: datetime = sa.Column(sa.DateTime(True), nullable=False)

    max_redemption_quota: int = sa.Column(sa.SmallInteger, nullable=False)
    minimum_purchase_amount: float = sa.Column(sa.Double(precision=2), nullable=False)
    discount_amount: float = sa.Column(sa.Double(precision=2), nullable=False)

    available_for_general_public: bool = sa.Column(sa.Boolean, default=False, nullable=False)
    first_purchase_only: bool = sa.Column(sa.Boolean, default=False, nullable=False)

    redemptions = relationship(Redemptions, backref="coupon")

    @property
    def expiration_date_as_unix(self) -> int:
        return floor(self.expiration_date.timestamp())

    def prepare_to_export(self) -> None:
        self.expiration_date = self.expiration_date_as_unix
