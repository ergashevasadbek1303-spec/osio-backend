"""Category schemas."""

from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


class CategoryCreate(BaseModel):
    """Kategoriya yaratish."""
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    display_order: int = 0
    is_active: bool = True

    @field_validator("name_uz", "name_ru", "name_en")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Nom kamida 2 ta belgi bo'lishi kerak")
        return v.strip()


class CategoryUpdate(BaseModel):
    """Kategoriya tahrirlash."""
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    image_url: Optional[str] = None
    display_order: Optional[int] = None
    is_active: Optional[bool] = None


class CategoryResponse(BaseModel):
    """Kategoriya response."""
    id: int
    name_uz: str
    name_ru: str
    name_en: str
    slug: str
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    image_url: Optional[str]
    display_order: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
