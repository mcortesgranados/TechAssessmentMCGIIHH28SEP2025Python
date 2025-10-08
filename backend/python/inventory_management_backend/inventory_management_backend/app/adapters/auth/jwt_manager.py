from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTManager:
    """
    JWTManager provides utilities for creating and verifying JSON Web Tokens (JWTs),
    and for securely hashing and verifying user passwords.

    Methods
    -------
    create_access_token(data: dict, expires_delta: timedelta = None) -> str
        Creates a JWT access token with an optional expiration delta.

    verify_access_token(token: str) -> dict | None
        Verifies a JWT access token and returns its payload if valid, else None.

    get_password_hash(password: str) -> str
        Hashes a plaintext password for secure storage.

    verify_password(plain_password: str, hashed_password: str) -> bool
        Verifies a plaintext password against a hashed password.
    """

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = None):
        """
        Create a JWT access token.

        Parameters
        ----------
        data : dict
            The payload data to encode in the JWT token.
        expires_delta : timedelta, optional
            The time duration after which the token expires. If not provided, uses
            the default expiration from settings.

        Returns
        -------
        str
            The encoded JWT token as a string.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    @staticmethod
    def verify_access_token(token: str):
        """
        Verify a JWT access token.

        Parameters
        ----------
        token : str
            The JWT token string to verify.

        Returns
        -------
        dict or None
            The decoded payload if verification succeeds; otherwise, None.
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except JWTError:
            return None

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Hash a plaintext password for secure storage.

        Parameters
        ----------
        password : str
            The plaintext password to hash.

        Returns
        -------
        str
            The hashed password.
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Parameters
        ----------
        plain_password : str
            The plaintext password to verify.
        hashed_password : str
            The previously hashed password to compare against.

        Returns
        -------
        bool
            True if the password matches the hash, False otherwise.
        """
        return pwd_context.verify(plain_password, hashed_password)