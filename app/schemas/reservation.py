"""Reservation schemas."""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime, date, time
import re


class ReservationCreate(BaseModel):
    """Bron qilish."""
    guest_name: str
    phone: str
    email: Optional[str] = None
    date: date
    time: time
    guests_count: int
    special_requests: Optional[str] = None

    @field_validator("guest_name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Ism kamida 2 ta belgi bo'lishi kerak")
        return v.strip()

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v):
        cleaned = re.sub(r"[\s\-\(\)]", "", v)
        if not re.match(r"^\+?[0-9]{9,15}$", cleaned):
            raise ValueError("Telefon raqam formati noto'g'ri")
        return cleaned

    @field_validator("guests_count")
    @classmethod
    def validate_guests(cls, v):
        if v < 1 or v > 50:
            raise ValueError("Mehmonlar soni 1 dan 50 gacha bo'lishi kerak")
        return v


class ReservationStatusUpdate(BaseModel):
    """Bron statusini o'zgartirish."""
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        if v not in ("pending", "confirmed", "cancelled"):
            raise ValueError("Status faqat pending, confirmed yoki cancelled bo'lishi mumkin")
        return v


class ReservationResponse(BaseModel):
    """Bron response."""
    id: int
    guest_name: str
    phone: str
    email: Optional[str]
    date: date
    time: time
    guests_count: int
    special_requests: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
