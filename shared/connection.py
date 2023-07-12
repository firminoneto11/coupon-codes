from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import _BaseDeclaration


class DBConnectionHandler:
    session: AsyncSession

    def __init__(self) -> None:
        self._engine = None
        self._session_maker = None

    def init(self, url: str) -> None:
        self._engine = create_async_engine(url=url)
        self._session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def close(self) -> None:
        await self.engine.dispose()

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise ValueError("Engine is None. Can not proceed.")
        return self._engine

    @property
    def session_maker(self) -> async_sessionmaker[AsyncSession]:
        if self._session_maker is None:
            raise ValueError("Session maker is None. Can not proceed.")
        return self._session_maker

    async def execute_ddl(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(_BaseDeclaration.metadata.drop_all)
            await conn.run_sync(_BaseDeclaration.metadata.create_all)


async def make_db_session():
    db_session = database.session_maker()
    try:
        yield db_session
    except Exception as exc:
        await db_session.rollback()
        raise exc
    finally:
        await db_session.close()
        del db_session


database = DBConnectionHandler()
