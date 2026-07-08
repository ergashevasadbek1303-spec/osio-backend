"""User model — Admin foydalanuvchilar."""

import uuid
from datetime import datetime, timezone
# pyrefly: ignore [missing-import]
from sqlalchemy import String, Boolean, DateTime
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=generate_uuid
    )
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String(20), default="admin")  # admin / superadmin
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_utc_now
    )

    def __repr__(self) -> str:
        return f"<User(username={self.username}, role={self.role})>"
