"""
Osio Restaurant — Main Application Entry Point
FastAPI application factory with startup events.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# pyrefly: ignore [missing-import]
from sqlalchemy import select

from app.core.config import settings
from app.core.database import create_tables, AsyncSessionLocal
from app.core.security import hash_password
from app.models import User, Category, MenuItem, Reservation, Contact
from app.api.v1 import auth, categories, menu_items, reservations, contacts
from app.api.v1 import analytics, recommendations


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup va shutdown events."""
    # === STARTUP ===
    print("[STARTUP] Osio Restaurant API ishga tushmoqda...")

    # Jadvallarni yaratish
    await create_tables()
    print("[DB] Database jadvallar yaratildi")

    # Ma'lumotlarni avtomatik to'ldirish (seeding)
    try:
        from seed import seed as run_seed
        await run_seed()
        print("[DB] Database avtomatik to'ldirildi/tekshirildi")
    except Exception as e:
        print(f"[DB] Seeding yuklashda xatolik: {e}")

    # Birinchi superadminni yaratish (agar mavjud bo'lmasa)
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.role == "superadmin")
        )
        superadmin = result.scalar_one_or_none()

        if not superadmin:
            superadmin = User(
                username=settings.FIRST_SUPERADMIN_USERNAME,
                email=settings.FIRST_SUPERADMIN_EMAIL,
                hashed_password=hash_password(settings.FIRST_SUPERADMIN_PASSWORD),
                role="superadmin",
            )
            session.add(superadmin)
            await session.commit()
            print(f"[DB] Superadmin yaratildi: {settings.FIRST_SUPERADMIN_USERNAME}")
        else:
            print(f"[DB] Superadmin allaqachon mavjud")

    yield

    # === SHUTDOWN ===
    print("[SHUTDOWN] Osio Restaurant API to'xtatilmoqda...")


# FastAPI app yaratish
app = FastAPI(
    title=settings.APP_NAME,
    description="Osio Restaurant — Zamonaviy restoran boshqaruv tizimi API",
    version="1.0.0",
    lifespan=lifespan,
    # Production'da docs yashirish
    docs_url=None if settings.is_production else "/docs",
    redoc_url=None if settings.is_production else "/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files (frontend)
import os
frontend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# API v1 routerlarini ro'yxatdan o'tkazish
API_V1_PREFIX = "/api/v1"
app.include_router(auth.router, prefix=API_V1_PREFIX)
app.include_router(categories.router, prefix=API_V1_PREFIX)
app.include_router(menu_items.router, prefix=API_V1_PREFIX)
app.include_router(reservations.router, prefix=API_V1_PREFIX)
app.include_router(contacts.router, prefix=API_V1_PREFIX)
app.include_router(analytics.router, prefix=API_V1_PREFIX)
app.include_router(recommendations.router, prefix=API_V1_PREFIX)


@app.get("/")
async def root():
    """API health check."""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs" if not settings.is_production else "disabled",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
