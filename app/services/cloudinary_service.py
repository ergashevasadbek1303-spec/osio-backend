"""
Osio Restaurant — Cloudinary Service
Rasm yuklash va o'chirish. Faqat rasm formatlari ruxsat etiladi.
"""

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

# Cloudinary konfiguratsiyasi
cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True,
)

# Ruxsat etilgan formatlar va maksimal hajm
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp", "gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def _validate_image(file: UploadFile):
    """Fayl turini va hajmini tekshiradi."""
    # Extension tekshirish
    if file.filename:
        ext = file.filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Faqat {', '.join(ALLOWED_EXTENSIONS)} formatlariga ruxsat beriladi",
            )

    # Content type tekshirish
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Faqat rasm fayllari yuklash mumkin",
        )


async def upload_image(file: UploadFile, folder: str = "osio/menu") -> dict:
    """
    Rasmni Cloudinary'ga yuklaydi. Agar Cloudinary sozlanmagan bo'lsa, dummy rasm qaytaradi.
    Returns: {"url": "...", "public_id": "..."}
    """
    _validate_image(file)

    # Cloudinary sozlanmagan bo'lsa, dummy rasm qaytarish
    if settings.CLOUDINARY_CLOUD_NAME == "disabled" or not settings.CLOUDINARY_CLOUD_NAME:
        return {
            "url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80",
            "public_id": None,
        }

    # Fayl hajmini tekshirish
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Fayl hajmi 5 MB dan oshmasligi kerak",
        )

    try:
        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="image",
            transformation=[
                {"quality": "auto", "fetch_format": "auto"},
            ],
        )
        return {
            "url": result["secure_url"],
            "public_id": result["public_id"],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Rasm yuklashda xatolik: {str(e)}",
        )


async def delete_image(public_id: str) -> bool:
    """Rasmni Cloudinary'dan o'chiradi."""
    if not public_id:
        return False

    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception:
        return False
