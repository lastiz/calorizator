from argon2 import PasswordHasher as _PW
from argon2.exceptions import VerificationError
import secrets


class Hasher:
    """
    Main Password hasher in APP
    """

    _context = _PW()

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        try:
            cls._context.verify(hashed_password, plain_password)
        except VerificationError:
            return False
        return True

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls._context.hash(password)

    def generate_session_token(self) -> str:
        return secrets.token_urlsafe(64)
