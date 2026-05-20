from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain password matches a bcrypt hashed password.

    Args:
        plain_password (str): Raw password provided by the user.
        hashed_password (str): Stored bcrypt hashed password.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


def get_password_hash(password: str) -> str:
    """
    Generates a bcrypt hash for a password.

    Note:
        Password is truncated to 72 bytes due to bcrypt limitation.

    Args:
        password (str): Raw password.

    Returns:
        str: Bcrypt hashed password (UTF-8 decoded string).
    """
    safe_password = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(safe_password, salt)

    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): Payload data to encode in the token.
        expires_delta (timedelta | None): Custom expiration time.

    Returns:
        str: Encoded JWT access token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    to_encode.update(
        {
            "exp": expire,
            "type": "access",
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def create_refresh_token(data: dict) -> str:
    """
    Creates a JWT refresh token.

    Args:
        data (dict): Payload data to encode in the token.

    Returns:
        str: Encoded JWT refresh token.
    """
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update(
        {
            "exp": expire,
            "type": "refresh",
        }
    )

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_token(token: str, expected_type: str) -> dict | None:
    """
    Decodes and validates a JWT token.

    Args:
        token (str): JWT token string.
        expected_type (str): Expected token type ("access" or "refresh").

    Returns:
        dict | None: Decoded payload if valid, otherwise None.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        if payload.get("type") != expected_type:
            return None

        return payload

    except JWTError:
        return None
