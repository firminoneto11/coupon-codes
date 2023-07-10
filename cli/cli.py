import asyncio as aio

from uvicorn import run as run_app
from uvloop import install

from conf import settings

from .exceptions import InvalidCommandError


def execute_from_command_line(command: str, port: int = 8000) -> None:
    """
    'runserver': Run the development server

    '--port': Set this if you want to use a different port when running the 'runserver' command. Defaults to 8000
    """
    install()

    match cmd := command.lower():
        case "runserver":
            return runserver(port=port)
        case "migrate":
            return
        case _:
            raise InvalidCommandError(f"Command {cmd!r} is invalid.")


def runserver(port: int) -> None:
    run_app(settings.ASGI_APP, log_level="info", reload=True, port=port)
