from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import declarative_base

from .utils import utcnow

if TYPE_CHECKING:
    from sqlalchemy.orm.decl_api import DeclarativeMeta

    BaseDeclaration: DeclarativeMeta


class TimeStampedBaseModel(BaseDeclaration := declarative_base()):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    created_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.current_timestamp(),
    )

    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.current_timestamp(),
        onupdate=utcnow,
    )
