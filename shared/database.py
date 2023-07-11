from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import BaseDeclaration


class AsyncDatabase:
    def __init__(self) -> None:
        self._engine = None
        self._db_session = None

    def init(self, url: str) -> None:
        self._engine = create_async_engine(url=url)
        self._db_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def close(self) -> None:
        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is None. Can not proceed.")
        return self._engine

    @property
    def db_session(self) -> async_sessionmaker[AsyncSession]:
        if self._db_session is None:
            raise ValueError("DB Session is None. Can not proceed.")
        return self._db_session

    async def execute_ddl(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseDeclaration.metadata.drop_all)
            await conn.run_sync(BaseDeclaration.metadata.create_all)


async def database_access():
    async with database.db_session() as db_session:
        async with db_session.begin():
            yield db_session


database = AsyncDatabase()
