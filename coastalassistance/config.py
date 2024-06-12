import pathlib

import environ
from pydantic_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))


class Settings(BaseSettings):
    bot_token: str = env("BOT_TOKEN")
    admin_id: str = env("ADMIN_ID")
    yandex_maps_token: str = env("YANDEX_MAPS_TOKEN")

    db_username: str = env("POSTGRESQL_USERNAME")
    db_password: str = env("POSTGRESQL_PASSWORD")
    db_host: str = env("POSTGRESQL_HOST")
    db_port: str = env("POSTGRESQL_PORT")
    db_name: str = env("POSTGRESQL_NAME")


settings = Settings()
