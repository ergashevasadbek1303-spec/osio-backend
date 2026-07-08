"""
Osio Restaurant — Reservations Router
Bron qilish va boshqarish.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.reservation import Reservation
from app.models.user import User
from app.schemas.reservation import (
    ReservationCreate, ReservationStatusUpdate, ReservationResponse,
)

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=ReservationResponse, status_code=201)
async def create_reservation(
    data: ReservationCreate,
    db: AsyncSession = Depends(get_db),
):
    """Stol band qilish — Public."""
    reservation = Reservation(
        guest_name=data.guest_name,
        phone=data.phone,
        email=data.email,
        date=data.date,
        time=data.time,
        guests_count=data.guests_count,
        special_requests=data.special_requests,
    )
    db.add(reservation)
    await db.flush()
    await db.refresh(reservation)

    return reservation


@router.get("/", response_model=List[ReservationResponse])
async def get_reservations(
    status_filter: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Barcha bronlarni ko'rish — Admin only."""
    query = select(Reservation)

    if status_filter:
        query = query.where(Reservation.status == status_filter)

    query = query.order_by(Reservation.created_at.desc())
    result = await db.execute(query)

    return result.scalars().all()


@router.patch("/{reservation_id}/status", response_model=ReservationResponse)
async def update_reservation_status(
    reservation_id: int,
    data: ReservationStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bron statusini o'zgartirish — Admin only."""
    result = await db.execute(
        select(Reservation).where(Reservation.id == reservation_id)
    )
    reservation = result.scalar_one_or_none()

    if not reservation:
        raise HTTPException(status_code=404, detail="Bron topilmadi")

    reservation.status = data.status
    await db.flush()
    await db.refresh(reservation)

    return reservation


@router.delete("/{reservation_id}", status_code=204)
async def delete_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Bronni o'chirish — Admin only."""
    result = await db.execute(
        select(Reservation).where(Reservation.id == reservation_id)
    )
    reservation = result.scalar_one_or_none()

    if not reservation:
        raise HTTPException(status_code=404, detail="Bron topilmadi")

    await db.delete(reservation)

