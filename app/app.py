from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.db import db_setup
from app.config import settings
from app.auth.routes import router as auth_router
from app.ingredients.routes import router as ingredient_router
from app.products.routes import router as product_router
from app.core.exceptions import BaseAppError, app_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    from tortoise import Tortoise

    await Tortoise.generate_schemas(safe=True)
    yield


def create_app() -> FastAPI:
    """
    Инициализация приложения
    """
    app = FastAPI(
        title=settings.APP_TITLE,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
        exception_handlers={
            BaseAppError: app_error_handler,
        },
    )

    ### ROUTES ###
    app.include_router(auth_router, prefix="/api")
    app.include_router(ingredient_router, prefix="/api")
    app.include_router(product_router, prefix="/api")

    ### SETUP ORM ###
    db_setup(app)

    return app
