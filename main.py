import asyncio as aio

from typer import Typer
from uvicorn import run
from uvloop import install

from conf import settings
from shared.connection import conn

cli = Typer()


async def _run_migrate() -> None:
    conn.init()
    await conn.execute_ddl()
    await conn.close()


@cli.command()
def migrate() -> None:
    """
    Creates all the tables into the database. Keep in mind that it drops the current tables and re-creates them.
    """
    install()

    for imp in [f"from apps.{app} import models" for app in settings.APPS]:
        exec(imp)

    aio.run(_run_migrate())


@cli.command()
def runserver(log_level: str = "info", reload: bool = True, port: int = 8000) -> None:
    """Runs the development server"""
    run(settings.ASGI_APP, log_level=log_level, reload=reload, port=port)


if __name__ == "__main__":
    cli()
