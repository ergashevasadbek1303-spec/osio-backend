"""User schemas — Input validation va response formatting."""

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
import re


class UserCreate(BaseModel):
    """Admin yaratish uchun schema."""
    username: str
    email: str
    password: str
    role: str = "admin"

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 50:
            raise ValueError("Username 3 dan 50 gacha belgi bo'lishi kerak")
        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError("Username faqat harf, raqam va _ bo'lishi mumkin")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError("Email formati noto'g'ri")
        return v.lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Parol kamida 8 ta belgi bo'lishi kerak")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v):
        if v not in ("admin", "superadmin"):
            raise ValueError("Role faqat 'admin' yoki 'superadmin' bo'lishi mumkin")
        return v


class UserLogin(BaseModel):
    """Login uchun schema."""
    username: str
    password: str


class UserResponse(BaseModel):
    """User response — parol qaytarilmaydi."""
    id: str
    username: str
    email: str
    is_active: bool
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Token yangilash uchun."""
    refresh_token: str
