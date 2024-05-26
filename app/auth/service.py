from fastapi import Depends
from fastapi.security import APIKeyHeader

from app.core.models import User
from app.utils import Hasher
from app.auth.exceptions import NotAuthenticatedError, EmailAlreadyExistsError, UsernameAlreadyExistsError


auth_scheme = APIKeyHeader(name="X-Auth", auto_error=False)


class AuthService:
    _hasher = Hasher()
    
    @property
    def hasher(self) -> Hasher:
        return self._hasher
    
    async def login_user(self, username: str, password: str) -> dict:
        """
        1. Checks username and password
        2. Creates and saves token for user
        Returns token
        """
        user = await User.get_or_none(username=username)
        not_authorized = NotAuthenticatedError()

        if not user:
            raise not_authorized
        
        if not self.hasher.verify_password(password, user.hashed_password):
            raise not_authorized
        
        token = self.hasher.generate_session_token()
        user.token = token
        await user.save(update_fields=["token"])
        return {"token": token}
        
    async def logout_user(self, user: User) -> None:
        """
        Logout user, deletes user auth token from database
        """
        user.token = ""
        await user.save(update_fields=["token"])
    
    async def register_user(self, username: str, password: str, email: str) -> User:
        """
        Create user in db
        Returns created user
        """
        if await self.username_exists(username=username):
            raise UsernameAlreadyExistsError()
        
        if await self.email_exists(email):
            raise EmailAlreadyExistsError()
        
        hashed_password = self.hasher.hash_password(password)
        user = await User.create(username=username, hashed_password=hashed_password, email=email)
        return user
    
    async def username_exists(self, username: str) -> bool:
        """
        Checks if username already exists in database
        """
        return await User.exists(username=username)
    
    async def email_exists(self, email: str) -> bool:
        """
        Checks if email already exists in database
        """
        return await User.exists(email=email)
