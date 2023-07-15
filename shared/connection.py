from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from conf import settings

from .models import _BaseDeclaration

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class DBConnectionHandler:
    _sessions_tracker: set["AsyncSession"]

    def __init__(self) -> None:
        self._engine = None
        self._make_session = None
        self._sessions_tracker = set()

    def init(self, sqlite: bool = False) -> None:
        if sqlite:  # pragma: no branch
            self._engine = create_async_engine(
                url=settings.AIOSQLITE_URL, connect_args={"check_same_thread": False}
            )
        else:
            self._engine = create_async_engine(url=settings.ASYNCPG_URL)  # pragma: no cover

        self._make_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def close(self) -> None:
        for ses in self._sessions_tracker:
            await ses.close()
        await self.engine.dispose()

    @property
    def engine(self) -> "AsyncEngine":
        if self._engine is None:
            raise ValueError("Engine is None. Can not proceed.")
        return self._engine

    @property
    def make_session(self) -> async_sessionmaker["AsyncSession"]:
        if self._make_session is None:
            raise ValueError("Session maker is None. Can not proceed.")
        return self._make_session

    async def get_db_session(self):
        self._sessions_tracker.add(ses := self.make_session())
        try:
            yield ses
        except Exception as exc:
            await ses.rollback()
            raise exc
        finally:
            self._sessions_tracker.remove(ses)
            await ses.close()
            del ses

    async def execute_ddl(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(_BaseDeclaration.metadata.drop_all)
            await conn.run_sync(_BaseDeclaration.metadata.create_all)


conn = DBConnectionHandler()
