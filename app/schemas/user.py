from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """
    Base schema for user data.

    Defines shared attributes used across user-related schemas.
    """

    email: str


class UserCreate(UserBase):
    """
    Schema used for creating a new user account.

    Includes the required password field for registration.
    """

    password: str


class UserResponse(UserBase):
    """
    Schema returned by the API when representing a user.

    Exposes safe, non-sensitive user information only.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    created_at: datetime
