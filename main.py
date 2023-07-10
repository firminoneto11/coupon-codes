from typer import Typer
from uvicorn import run
from uvloop import install

from conf import settings

app = Typer()


@app.command()
def migrate() -> None:
    """
    Creates all the tables into the database. Keep in mind that it drops the current tables and re-creates them.
    """
    install()


@app.command()
def runserver(log_level: str = "info", reload: bool = True, port: int = 8000) -> None:
    """Runs the development server"""
    run(settings.ASGI_APP, log_level=log_level, reload=reload, port=port)


if __name__ == "__main__":
    app()
