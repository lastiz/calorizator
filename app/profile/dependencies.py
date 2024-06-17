from app.profile.service import ProfileService


def get_profile_service() -> ProfileService:
    return ProfileService()
