from pathlib import Path as _Path

from dynaconf import Dynaconf as _Dynaconf
from dynaconf import Validator as _Validator

envs = _Dynaconf(
    envvar_prefix="CC",
    load_dotenv=True,
    validators=[
        _Validator("ASGI_APP", default="config.asgi:app"),
        _Validator("DEBUG", cast=bool),
    ],
)

BASE_DIR = _Path(__file__).resolve().parent.parent.parent

ASYNCPG_URL = envs.asyncpg_url

ASGI_APP = envs.asgi_app

DEBUG = envs.debug

APP_TITLE = "Coupon Codes"

ALLOWED_HOSTS = envs.allowed_hosts.split(", ")

ALLOWED_ORIGINS = envs.allowed_origins.split(", ")

APPS = ["core"]
