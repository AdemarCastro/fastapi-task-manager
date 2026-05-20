from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha plain corresponde ao hash bcrypt."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    """Gera hash bcrypt da senha (trunca para 72 bytes, limite do algoritmo)."""
    safe_password = password.encode("utf-8")[:72]
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(safe_password, salt)
    return hashed.decode("utf-8")


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str, expected_type: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            return None
        return payload
    except JWTError:
        return None
