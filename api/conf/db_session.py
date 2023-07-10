from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from conf import settings
from shared.models import BaseDeclaration


def create_tables() -> None:
    """
    This function creates all tables for every model defined. Beware that it drops
    previously created tables and then recreates them.
    """
    BaseDeclaration.metadata.drop_all(engine)
    BaseDeclaration.metadata.create_all(engine)


engine = create_async_engine(url=settings.ASYNCPG_URL)

session = async_sessionmaker(engine)
