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

APP_TITLE = "Coupon Codes"

ALLOWED_HOSTS = envs.allowed_hosts.split(", ")

ALLOWED_ORIGINS = envs.allowed_origins.split(", ")

APPS = ["core"]
