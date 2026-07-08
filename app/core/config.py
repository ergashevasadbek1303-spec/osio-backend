"""
Osio Restaurant — Core Configuration
Barcha konfiguratsiyalar .env fayldan o'qiladi (Pydantic Settings orqali).
Hech qanday secret hardcode qilinmaydi.
"""

# pyrefly: ignore [missing-import]
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings — .env fayldan yuklanadi."""

    # ---------- App ----------
    APP_NAME: str = "Osio Restaurant"
    APP_ENV: str = "development"

    # ---------- Database (Neon PostgreSQL or SQLite) ----------
    DATABASE_URL: str = "sqlite+aiosqlite:///./osio_restaurant.db"

    # ---------- JWT ----------
    JWT_SECRET_KEY: str = "localdevsecretkeyforosiodashboard2026!"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ---------- Cloudinary (ixtiyoriy) ----------
    CLOUDINARY_CLOUD_NAME: str = "disabled"
    CLOUDINARY_API_KEY: str = "disabled"
    CLOUDINARY_API_SECRET: str = "disabled"

    # ---------- CORS ----------
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8000"

    # ---------- First Superadmin ----------
    FIRST_SUPERADMIN_USERNAME: str = "admin"
    FIRST_SUPERADMIN_EMAIL: str = "admin@osio.uz"
    FIRST_SUPERADMIN_PASSWORD: str = "change-this-password-immediately"

    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins ro'yxatini qaytaradi."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
