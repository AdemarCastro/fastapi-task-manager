from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class User(Base):
    """
    Represents a user entity in the system.

    This model stores authentication and account-related information,
    including credentials, status, and relationships with tasks.

    A user can own multiple tasks.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    tasks = relationship("Task", back_populates="owner")
