from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    """
    Schema for user registration.

    Used to validate data when creating a new user account.
    """

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """
    Schema for user authentication.

    Used to validate login credentials.
    """

    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Authentication token response schema.

    Returned after successful login or token refresh.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """
    Schema for refreshing authentication tokens.

    Used to obtain new access and refresh tokens using a valid refresh token.
    """

    refresh_token: str
