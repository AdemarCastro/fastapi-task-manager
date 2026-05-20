from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    is_done: Mapped[bool] = mapped_column(default=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    owner = relationship("User", back_populates="tasks")
