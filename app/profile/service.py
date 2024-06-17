from app.core.models import User

class ProfileService:
    """
    Business logic for profile domain
    """
    
    async def get_profile(self, user: User) -> User:
        """
        Returns profile
        TODO: add some more information
        """
        return user