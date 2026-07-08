"""MenuItem schemas."""

from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime


class MenuItemCreate(BaseModel):
    """Taom qo'shish."""
    category_id: int
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    price: float
    is_available: bool = True
    is_featured: bool = False

    @field_validator("name_uz", "name_ru", "name_en")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Nom kamida 2 ta belgi bo'lishi kerak")
        return v.strip()

    @field_validator("price")
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError("Narx 0 dan katta bo'lishi kerak")
        return round(v, 2)


class MenuItemUpdate(BaseModel):
    """Taom tahrirlash."""
    category_id: Optional[int] = None
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    name_en: Optional[str] = None
    description_uz: Optional[str] = None
    description_ru: Optional[str] = None
    description_en: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    is_featured: Optional[bool] = None


class MenuItemResponse(BaseModel):
    """Taom response."""
    id: int
    category_id: int
    name_uz: str
    name_ru: str
    name_en: str
    description_uz: Optional[str]
    description_ru: Optional[str]
    description_en: Optional[str]
    price: float
    image_url: Optional[str]
    is_available: bool
    is_featured: bool
    created_at: datetime

    class Config:
        from_attributes = True
