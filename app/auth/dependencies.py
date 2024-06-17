from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.core.models import User
from app.auth.exceptions import NotAuthenticatedError


async def get_current_user(
    token: Annotated[str, Depends(APIKeyHeader(name="X-Auth", auto_error=False))]
) -> User:
    """
    Authenticates user by token
    Returns user
    """
    user = await User.get_or_none(token=token)

    if not user:
        raise NotAuthenticatedError(msg="Invalid authorization token", fields=["token"])

    return user
