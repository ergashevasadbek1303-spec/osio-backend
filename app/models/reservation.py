"""Reservation model — Stol band qilish."""

from datetime import datetime, date, time, timezone
from sqlalchemy import String, Text, Integer, Date, Time, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    guest_name: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    time: Mapped[time] = mapped_column(Time, nullable=False)
    guests_count: Mapped[int] = mapped_column(Integer, nullable=False)
    special_requests: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending / confirmed / cancelled
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"<Reservation(guest={self.guest_name}, date={self.date}, status={self.status})>"
