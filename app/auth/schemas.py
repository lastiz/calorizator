from pydantic import BaseModel, Field, EmailStr


class LoginScheme(BaseModel):
    """
    Login scheme
    """
    username: str
    password: str


class TokenScheme(BaseModel):
    """
    Authorization token scheme
    """
    token: str
    

class RegisterScheme(BaseModel):
    """
    Scheme to register user
    """
    username: str = Field(min_length=4, max_length=32)
    email: EmailStr
    password: str = Field(max_length=32, min_length=8)


class RegisteredUserScheme(BaseModel):
    """
    Response on register user scheme
    """
    username: str
    email: str


class GenericResponseScheme(BaseModel):
    """
    Response to logout user
    """
    status_code: int
    msg: str