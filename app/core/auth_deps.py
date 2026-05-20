from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Retrieves the currently authenticated user from a JWT access token.

    This dependency:
    - Decodes and validates the JWT token
    - Extracts the user ID from the token payload
    - Fetches the user from the database
    - Ensures the user is active

    Args:
        token (str): JWT access token extracted from Authorization header.
        db (Session): Database session dependency.

    Raises:
        HTTPException: If the token is invalid, expired, or the user
        does not exist or is inactive.

    Returns:
        User: The authenticated user instance.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token, expected_type="access")

    if not payload or "sub" not in payload:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(payload["sub"])).first()

    if not user or not user.is_active:
        raise credentials_exception

    return user
