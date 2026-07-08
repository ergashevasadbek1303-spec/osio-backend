"""
Osio Restaurant — Categories Router
CRUD operatsiyalar — kategoriyalar boshqaruvi.
"""

import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


def generate_slug(name: str) -> str:
    """Nomdan URL-friendly slug yaratadi."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s-]+", "-", slug)
    return slug


@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    active_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Barcha kategoriyalarni qaytaradi."""
    query = select(Category)
    if active_only:
        query = query.where(Category.is_active == True)
    query = query.order_by(Category.display_order)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    """Bitta kategoriya."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")

    return category


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Yangi kategoriya qo'shish — Admin only."""
    slug = generate_slug(data.name_en)

    # Slug unique tekshirish
    existing = await db.execute(select(Category).where(Category.slug == slug))
    if existing.scalar_one_or_none():
        slug = f"{slug}-{int(import_time())}"

    category = Category(
        name_uz=data.name_uz,
        name_ru=data.name_ru,
        name_en=data.name_en,
        slug=slug,
        description_uz=data.description_uz,
        description_ru=data.description_ru,
        description_en=data.description_en,
        image_url=data.image_url,
        display_order=data.display_order,
        is_active=data.is_active,
    )
    db.add(category)
    await db.flush()
    await db.refresh(category)

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kategoriyani tahrirlash — Admin only."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)

    # Agar nom o'zgarsa, slugni yangilash
    if "name_en" in update_data:
        category.slug = generate_slug(update_data["name_en"])

    await db.flush()
    await db.refresh(category)

    return category


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Kategoriyani o'chirish — Admin only."""
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")

    await db.delete(category)


def import_time():
    """Vaqtni import qiladi (slug unique qilish uchun)."""
    from time import time
    return time()
