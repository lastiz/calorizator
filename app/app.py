from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import db_setup
from app.config import settings
from app.auth.routes import router as auth_router
from app.ingredients.routes import router as ingredient_router
from app.products.routes import router as product_router
from app.profile.routes import router as profile_router
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
    app.include_router(profile_router, prefix="/api")

    ### CORS ###
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    ### SETUP ORM ###
    db_setup(app)

    return app
