from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, create_refresh_token, decode_token
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import Token, TokenRefresh, UserLogin, UserRegister
from app.services.user_service import authenticate_user, create_user, get_user_by_email

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)


# ------------------------------------------------------------
# REGISTER
# ------------------------------------------------------------
@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description=(
        "Creates a new user account in the system.\n\n"
        "The email must be unique. If the email already exists, "
        "the request will be rejected."
    ),
)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    if get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Email is already registered",
        )

    user = create_user(db, user_in.email, user_in.password)

    return {
        "message": "User created successfully",
        "user_id": user.id,
    }


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------
@router.post(
    "/login",
    response_model=Token,
    summary="Authenticate user",
    description=(
        "Authenticates a user and returns JWT tokens.\n\n"
        "Returns:\n"
        "- access_token: used to authenticate requests\n"
        "- refresh_token: used to generate new access tokens"
    ),
)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_in.email, user_in.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Inactive user",
        )

    access_token = create_access_token({"sub": str(user.id), "email": user.email})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


# ------------------------------------------------------------
# REFRESH TOKEN
# ------------------------------------------------------------
@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh JWT tokens",
    description=(
        "Generates new JWT tokens using a valid refresh token.\n\n"
        "If the refresh token is invalid or expired, "
        "the request will be rejected."
    ),
)
def refresh_token(token_data: TokenRefresh, db: Session = Depends(get_db)):
    payload = decode_token(
        token_data.refresh_token,
        expected_type="refresh",
    )

    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    user = db.query(User).filter(User.id == int(payload["sub"])).first()

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not found or inactive",
        )

    new_access = create_access_token({"sub": str(user.id), "email": user.email})
    new_refresh = create_refresh_token({"sub": str(user.id)})

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
    }
