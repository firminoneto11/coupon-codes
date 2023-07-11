from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from shared.models import TimeStampedBaseModel

from .enums import DiscountTypesEnum


class Redemptions(TimeStampedBaseModel):
    if TYPE_CHECKING:
        coupon: "Coupons"

    __tablename__ = "redemptions"

    coupon_id = sa.Column(sa.BigInteger, sa.ForeignKey("coupons.id"), nullable=False)
    total_purchase_amount = sa.Column(sa.Double(precision=2), nullable=False)
    is_first_purchase = sa.Column(sa.Boolean, nullable=False)


class Coupons(TimeStampedBaseModel):
    __tablename__ = "coupons"

    code = sa.Column(sa.String(300), unique=True, nullable=False)
    type = sa.Column(sa.Enum(DiscountTypesEnum), nullable=False, name="type_enum")

    expiration_date = sa.Column(sa.DateTime(True), nullable=False)

    max_redemption_quota = sa.Column(sa.SmallInteger, nullable=False)
    minimum_purchase_amount = sa.Column(sa.Double(precision=2), nullable=False)
    discount_amount = sa.Column(sa.Double(precision=2), nullable=False)

    general_public = sa.Column(sa.Boolean, default=False, nullable=False)
    first_purchase = sa.Column(sa.Boolean, default=False, nullable=False)

    redemptions = relationship(Redemptions, backref="coupon")
