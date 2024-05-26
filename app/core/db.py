from tortoise import BaseDBAsyncClient, Tortoise
from tortoise.contrib.fastapi import register_tortoise
from fastapi import FastAPI

from app.config import settings


def get_db() -> BaseDBAsyncClient:
    return Tortoise.get_connection("default")


def db_setup(app: FastAPI):
    """
    Initiates tortoise ORM
    """
    config = {
        "connections": {
            "default": settings.DB_URL,
        },
        "apps": {
            "models": {
                "models": ["app.core.models"],
                "default_connection": "default",
            }
        },
        "use_tz": False,
        "timezone": "Europe/Moscow",
    }
    register_tortoise(app, config)
