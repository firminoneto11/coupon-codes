from pathlib import Path

from dynaconf import Dynaconf, Validator

envs = Dynaconf(
    envvar_prefix="CC",
    load_dotenv=True,
    validators=[
        Validator("ASGI_APP", default="api.conf.asgi:app"),
        Validator("DEBUG", cast=bool),
    ],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ASYNCPG_URL = envs.asyncpg_url

ASGI_APP = envs.asgi_app

DEBUG = envs.debug
