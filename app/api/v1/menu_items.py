"""
Osio Restaurant — Menu Items Router
CRUD + Cloudinary rasm yuklash.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.menu_item import MenuItem
from app.models.user import User
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.services.cloudinary_service import upload_image, delete_image

router = APIRouter(prefix="/menu", tags=["Menu"])


@router.get("/", response_model=List[MenuItemResponse])
async def get_menu_items(
    category_id: Optional[int] = None,
    available_only: bool = True,
    db: AsyncSession = Depends(get_db),
):
    """Barcha taomlarni qaytaradi. Kategoriya bo'yicha filterlash mumkin."""
    query = select(MenuItem)

    if category_id:
        query = query.where(MenuItem.category_id == category_id)
    if available_only:
        query = query.where(MenuItem.is_available == True)

    query = query.order_by(MenuItem.created_at.desc())
    result = await db.execute(query)

    return result.scalars().all()


@router.get("/featured", response_model=List[MenuItemResponse])
async def get_featured_items(db: AsyncSession = Depends(get_db)):
    """Featured taomlarni qaytaradi."""
    result = await db.execute(
        select(MenuItem)
        .where(MenuItem.is_featured == True, MenuItem.is_available == True)
        .order_by(MenuItem.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{item_id}", response_model=MenuItemResponse)
async def get_menu_item(item_id: int, db: AsyncSession = Depends(get_db)):
    """Bitta taom."""
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Taom topilmadi")

    return item


@router.post("/", response_model=MenuItemResponse, status_code=201)
async def create_menu_item(
    category_id: int = Form(...),
    name_uz: str = Form(...),
    name_ru: str = Form(...),
    name_en: str = Form(...),
    description_uz: Optional[str] = Form(None),
    description_ru: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    price: float = Form(...),
    is_available: bool = Form(True),
    is_featured: bool = Form(False),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Yangi taom qo'shish + rasm yuklash — Admin only."""
    image_url = None
    cloudinary_public_id = None

    if image:
        result = await upload_image(image, folder="osio/menu")
        image_url = result["url"]
        cloudinary_public_id = result["public_id"]

    item = MenuItem(
        category_id=category_id,
        name_uz=name_uz,
        name_ru=name_ru,
        name_en=name_en,
        description_uz=description_uz,
        description_ru=description_ru,
        description_en=description_en,
        price=price,
        image_url=image_url,
        cloudinary_public_id=cloudinary_public_id,
        is_available=is_available,
        is_featured=is_featured,
    )
    db.add(item)
    await db.flush()
    await db.refresh(item)

    return item


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    category_id: Optional[int] = Form(None),
    name_uz: Optional[str] = Form(None),
    name_ru: Optional[str] = Form(None),
    name_en: Optional[str] = Form(None),
    description_uz: Optional[str] = Form(None),
    description_ru: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    is_available: Optional[bool] = Form(None),
    is_featured: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Taomni tahrirlash — Admin only."""
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Taom topilmadi")

    # Yangi rasm yuklansa, eskisini o'chirish
    if image:
        if item.cloudinary_public_id:
            await delete_image(item.cloudinary_public_id)
        upload_result = await upload_image(image, folder="osio/menu")
        item.image_url = upload_result["url"]
        item.cloudinary_public_id = upload_result["public_id"]

    # Faqat yuborilgan maydonlarni yangilash
    if category_id is not None:
        item.category_id = category_id
    if name_uz is not None:
        item.name_uz = name_uz
    if name_ru is not None:
        item.name_ru = name_ru
    if name_en is not None:
        item.name_en = name_en
    if description_uz is not None:
        item.description_uz = description_uz
    if description_ru is not None:
        item.description_ru = description_ru
    if description_en is not None:
        item.description_en = description_en
    if price is not None:
        item.price = price
    if is_available is not None:
        item.is_available = is_available
    if is_featured is not None:
        item.is_featured = is_featured

    await db.flush()
    await db.refresh(item)

    return item


@router.delete("/{item_id}", status_code=204)
async def delete_menu_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Taomni o'chirish — Cloudinary'dan ham rasmni o'chiradi. Admin only."""
    result = await db.execute(select(MenuItem).where(MenuItem.id == item_id))
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(status_code=404, detail="Taom topilmadi")

    # Cloudinary'dan rasmni o'chirish
    if item.cloudinary_public_id:
        await delete_image(item.cloudinary_public_id)

    await db.delete(item)
