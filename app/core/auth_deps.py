from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer(
    scheme_name="BearerAuth",
    description="JWT Access Token. Copy the token from /auth/login and paste it here.",
)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    """
    Extracts and validates the JWT token from the Authorization header.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token = credentials.credentials
        payload = decode_token(token, expected_type="access")

        if not payload or "sub" not in payload:
            raise credentials_exception

    except Exception:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(payload["sub"])).first()

    if not user or not user.is_active:
        raise credentials_exception

    return user
