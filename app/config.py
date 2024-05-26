from datetime import datetime
from functools import cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pygit2 import Repository


class Settings(BaseSettings):
    """
    Базовые настройки приложения
    """

    model_config = SettingsConfigDict(validate_default=False)

    DEBUG: bool = Field(default=False, alias="DEBUG_MODE")

    ### APP ###
    APP_TITLE: str = "Calorizator"
    APP_VERSION: str = Repository(".").head.shorthand
    APP_START_TIME: datetime = Field(default_factory=datetime.now)
    SERVICE_NAME: str = "calorizator"
    APP_PORT: int = 80
    TIMEZONE: str = "Europe/Moscow"

    ### POSTGRESQL ###
    PG_CRED: str

    @cached_property
    def DB_URL(self) -> str:
        PG_HOST, PG_PORT, PG_DATABASE, PG_USER, PG_PASS = self.PG_CRED.split(":")
        return f"asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"


settings = Settings()  # type: ignore
