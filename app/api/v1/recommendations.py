"""
Osio Restaurant — AI Taom Tavsiya Tizimi
Foydalanuvchi budjet va kategoriyasiga asoslangan aqlli tavsiyalar.
"""

from fastapi import APIRouter, Depends, Query
# pyrefly: ignore [missing-import]
from sqlalchemy.ext.asyncio import AsyncSession
# pyrefly: ignore [missing-import]
from sqlalchemy import select
from typing import Optional, List, Dict, Any

from app.core.database import get_db
from app.models.menu_item import MenuItem
from app.models.category import Category

router = APIRouter(prefix="/recommendations", tags=["AI Recommendations"])


@router.get("/")
async def get_recommendations(
    category_id: Optional[int] = Query(None, description="Kategoriya ID"),
    budget: Optional[float] = Query(None, description="Maksimal budjet (UZS)"),
    guests: Optional[int] = Query(None, description="Mehmonlar soni"),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    AI Taom Tavsiya — Public endpoint.
    Budjet, kategoriya va mehmonlar soniga qarab aqlli tavsiya beradi.
    """
    query = select(MenuItem, Category.name_uz.label("cat_uz"), Category.name_ru.label("cat_ru"), Category.name_en.label("cat_en")).join(
        Category, MenuItem.category_id == Category.id
    ).where(MenuItem.is_available == True)

    if category_id:
        query = query.where(MenuItem.category_id == category_id)

    if budget:
        query = query.where(MenuItem.price <= budget)

    result = await db.execute(query.order_by(MenuItem.is_featured.desc(), MenuItem.price.asc()))
    rows = result.all()

    # Tavsiya algoritmi
    recommendations = []
    featured = []
    affordable = []

    for row in rows:
        item = row[0]
        dish = {
            "id": item.id,
            "name_uz": item.name_uz,
            "name_ru": item.name_ru,
            "name_en": item.name_en,
            "description_uz": item.description_uz,
            "description_ru": item.description_ru,
            "description_en": item.description_en,
            "price": item.price,
            "image_url": item.image_url,
            "category_uz": row[1],
            "category_ru": row[2],
            "category_en": row[3],
            "is_featured": item.is_featured,
        }

        if item.is_featured:
            featured.append(dish)
        else:
            affordable.append(dish)

    # Aqlli tartiblash: featured birinchi, keyin narx bo'yicha
    recommendations = featured + affordable

    # Mehmonlar soni asosida tavsiya
    combo_suggestions = []
    if guests and guests >= 2 and budget:
        per_person_budget = budget / guests
        combo_query = select(MenuItem, Category.name_uz.label("cat_uz")).join(
            Category, MenuItem.category_id == Category.id
        ).where(
            MenuItem.is_available == True,
            MenuItem.price <= per_person_budget,
        ).order_by(MenuItem.is_featured.desc())

        combo_result = await db.execute(combo_query)

        # Har bir kategoriyadan 1 ta tanlash (menyu combo)
        seen_categories = set()
        for row in combo_result:
            item = row[0]
            if item.category_id not in seen_categories:
                seen_categories.add(item.category_id)
                combo_suggestions.append({
                    "id": item.id,
                    "name_uz": item.name_uz,
                    "name_ru": item.name_ru,
                    "name_en": item.name_en,
                    "price": item.price,
                    "category_uz": row[1],
                })

    # Budjet tahlili
    budget_analysis = None
    if budget:
        total_items = len(recommendations)
        if total_items > 0:
            avg_price = sum(r["price"] for r in recommendations) / total_items
            can_order = int(budget / avg_price) if avg_price > 0 else 0
            budget_analysis = {
                "budget": budget,
                "average_dish_price": round(avg_price),
                "estimated_dishes": can_order,
                "budget_status": (
                    "yetarli" if can_order >= 2
                    else "cheklangan" if can_order >= 1
                    else "yetarli emas"
                ),
            }

    return {
        "recommendations": recommendations[:10],
        "combo_menu": combo_suggestions[:5] if combo_suggestions else None,
        "budget_analysis": budget_analysis,
        "total_available": len(recommendations),
        "ai_tip": _generate_tip(recommendations, budget, guests),
    }


def _generate_tip(dishes: list, budget: Optional[float], guests: Optional[int]) -> str:
    """AI Tip — Foydalanuvchiga maslahat."""
    if not dishes:
        return "Hozircha tavsiya qilinadigan taomlar mavjud emas."

    featured = [d for d in dishes if d.get("is_featured")]

    if budget and budget >= 100000:
        return "💎 Premium tanlov! Bizning VIP taomlarimizni sinab ko'ring — Toshkent Oshi va Qo'y Kabob."
    elif budget and budget >= 50000:
        return "🌟 Ajoyib tanlov! Sizga to'liq o'zbek dasturxoni tavsiya etamiz."
    elif featured:
        return f"⭐ Bugungi tavsiya: {featured[0]['name_uz']} — eng mashhur taomimiz!"
    elif guests and guests >= 4:
        return "👨‍👩‍👧‍👦 Katta guruh uchun Palov va Sho'rva — eng yaxshi tanlov!"
    else:
        return "🍽 O'zbek milliy taomlari bilan tanishing — har biri yangi ta'm kashfiyoti!"
