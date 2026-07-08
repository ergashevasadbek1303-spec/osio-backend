"""
Osio Restaurant — Contacts Router
Aloqa xabarlari boshqaruvi.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.contact import Contact
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactResponse

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", response_model=ContactResponse, status_code=201)
async def create_contact(
    data: ContactCreate,
    db: AsyncSession = Depends(get_db),
):
    """Xabar yuborish — Public."""
    contact = Contact(
        name=data.name,
        email=data.email,
        subject=data.subject,
        message=data.message,
    )
    db.add(contact)
    await db.flush()
    await db.refresh(contact)

    return contact


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Barcha xabarlarni ko'rish — Admin only."""
    query = select(Contact)

    if unread_only:
        query = query.where(Contact.is_read == False)

    query = query.order_by(Contact.created_at.desc())
    result = await db.execute(query)

    return result.scalars().all()


@router.patch("/{contact_id}/read", response_model=ContactResponse)
async def mark_as_read(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xabarni o'qilgan deb belgilash — Admin only."""
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Xabar topilmadi")

    contact.is_read = True
    await db.flush()
    await db.refresh(contact)

    return contact


@router.delete("/{contact_id}", status_code=204)
async def delete_contact(
    contact_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Xabarni o'chirish — Admin only."""
    result = await db.execute(select(Contact).where(Contact.id == contact_id))
    contact = result.scalar_one_or_none()

    if not contact:
        raise HTTPException(status_code=404, detail="Xabar topilmadi")

    await db.delete(contact)

