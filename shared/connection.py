from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from config import settings

from .models import _BaseDeclaration


class DBConnectionHandler:
    def __init__(self) -> None:
        self._engine = None
        self._make_session = None

    def init(self, sqlite: bool = False) -> None:
        if sqlite:  # pragma: no branch
            self._engine = create_async_engine(
                url=settings.AIOSQLITE_URL, connect_args={"check_same_thread": False}
            )
        else:
            self._engine = create_async_engine(url=settings.ASYNCPG_URL)  # pragma: no cover

        self._make_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def close(self) -> None:
        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is None. Can not proceed.")
        return self._engine

    @property
    def make_session(self) -> async_sessionmaker[AsyncSession]:
        if self._make_session is None:
            raise ValueError("Session maker is None. Can not proceed.")
        return self._make_session

    async def execute_ddl(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(_BaseDeclaration.metadata.drop_all)
            await conn.run_sync(_BaseDeclaration.metadata.create_all)


async def make_db_session():
    db_session = connection.make_session()
    try:
        yield db_session
    except Exception as exc:
        await db_session.rollback()
        raise exc
    finally:
        await db_session.close()
        del db_session


connection = DBConnectionHandler()
