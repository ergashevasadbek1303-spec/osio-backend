"""MenuItem model — Taomlar."""

from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Boolean, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    name_uz: Mapped[str] = mapped_column(String(200), nullable=False)
    name_ru: Mapped[str] = mapped_column(String(200), nullable=False)
    name_en: Mapped[str] = mapped_column(String(200), nullable=False)
    description_uz: Mapped[str] = mapped_column(Text, nullable=True)
    description_ru: Mapped[str] = mapped_column(Text, nullable=True)
    description_en: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    cloudinary_public_id: Mapped[str] = mapped_column(String(200), nullable=True)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationship
    category = relationship("Category", back_populates="menu_items")

    def __repr__(self):
        return f"<MenuItem(name={self.name_uz}, price={self.price})>"
