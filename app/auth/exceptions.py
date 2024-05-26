from fastapi import status

from app.core.base import BaseAppError


class NotAuthenticatedError(BaseAppError):
    """
    Not authorized exception
    """
    status_code = status.HTTP_401_UNAUTHORIZED
    fields = ["username", "password"]
    msg = "Invalid username or password"


class EmailAlreadyExistsError(BaseAppError):
    """
    Email is already exists in database
    """
    status_code = status.HTTP_400_BAD_REQUEST
    fields = ["email"]
    msg = "Email is already exists"
    

class UsernameAlreadyExistsError(BaseAppError):
    """
    Username is already exists in database
    """
    status_code = status.HTTP_400_BAD_REQUEST
    fields = ["username"]
    msg = "Username is already exists"