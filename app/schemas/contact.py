"""Contact schemas."""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
import re


class ContactCreate(BaseModel):
    """Xabar yuborish."""
    name: str
    email: str
    subject: str
    message: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Ism kamida 2 ta belgi bo'lishi kerak")
        return v.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Email formati noto'g'ri")
        return v.lower()

    @field_validator("subject")
    @classmethod
    def validate_subject(cls, v):
        if len(v.strip()) < 3:
            raise ValueError("Mavzu kamida 3 ta belgi bo'lishi kerak")
        return v.strip()

    @field_validator("message")
    @classmethod
    def validate_message(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Xabar kamida 10 ta belgi bo'lishi kerak")
        return v.strip()


class ContactResponse(BaseModel):
    """Contact response."""
    id: int
    name: str
    email: str
    subject: str
    message: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True
