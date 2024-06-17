from typing import Annotated

from fastapi import APIRouter, Depends

from app.profile.schemas import ProfileSchema
from app.auth.dependencies import get_current_user, User
from app.profile.dependencies import get_profile_service, ProfileService


router = APIRouter(prefix="/profile", tags=["Profile operations"])


@router.get("/me", response_model=ProfileSchema)
async def get_profile_info(
    user: Annotated[User, Depends(get_current_user)],
    profile_service: Annotated[ProfileService, Depends(get_profile_service)],
):
    """
    Get full profile information
    """
    return await profile_service.get_profile(user)
