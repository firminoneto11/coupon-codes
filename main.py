import asyncio as aio

from typer import Typer
from uvicorn import run
from uvloop import install

from conf import settings
from shared.database import AsyncDatabase, database

cli = Typer()


async def _run_migrate(db: AsyncDatabase) -> None:
    db.init(settings.ASYNCPG_URL)
    await db.execute_ddl()
    await db.close()


@cli.command()
def migrate() -> None:
    """
    Creates all the tables into the database. Keep in mind that it drops the current tables and re-creates them.
    """
    install()
    aio.run(_run_migrate(db=database))


@cli.command()
def runserver(log_level: str = "info", reload: bool = True, port: int = 8000) -> None:
    """Runs the development server"""
    run(settings.ASGI_APP, log_level=log_level, reload=reload, port=port)


if __name__ == "__main__":
    cli()
