from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.auth.service import AuthService
from app.auth.schemas import (
    LoginScheme,
    TokenScheme,
    RegisterScheme,
    RegisteredUserScheme,
)
from app.auth.dependencies import get_current_user
from app.core.models import User
from app.generic.schemas import GenericResponse


router = APIRouter(prefix="/auth", tags=["Authorization"])


@router.post("/login", response_model=TokenScheme)
async def login(
    creds: LoginScheme,
):
    """
    Login into account and get auth token
    """
    return await AuthService().login_user(creds.username, creds.password)


@router.get("/logout")
async def logout(
    user: Annotated[User, Depends(get_current_user)],
) -> GenericResponse:
    """
    Logout from account
    """
    await AuthService().logout_user(user)
    return GenericResponse(status_code=200, msg="Successfully logout")


@router.post("/register", status_code=201, response_model=RegisteredUserScheme)
async def register(
    schema: RegisterScheme,
):
    """
    Regiser user account
    """
    return await AuthService().register_user(
        schema.username, schema.password, schema.email
    )
