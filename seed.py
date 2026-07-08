"""
Osio Restaurant — Database Seeding Script
"""

import os
import sys

# Ensure the backend directory is in the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
# pyrefly: ignore [missing-import]
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models import Category, MenuItem, User, Reservation, Contact
from datetime import date, time

async def seed():
    print("Database seeding boshlandi...")
    async with AsyncSessionLocal() as session:
        
        # 1. Add categories if they don't exist
        res_cat = await session.execute(select(Category))
        categories = res_cat.scalars().all()
        if not categories:
            c1 = Category(id=1, name_uz="Milliy Taomlar", name_ru="Национальные Блюда", name_en="National Dishes", slug="national-dishes", description_uz="Mazali milliy taomlar", description_ru="Вкусные национальные блюда", description_en="Delicious national dishes", display_order=1, is_active=True)
            c2 = Category(id=2, name_uz="Kaboblar", name_ru="Шашлыки", name_en="Kebabs", slug="kebabs", description_uz="Turli xil kaboblar", description_ru="Разнообразные шашлыки", description_en="Various types of kebabs", display_order=2, is_active=True)
            c3 = Category(id=3, name_uz="Suyuq Taomlar", name_ru="Супы", name_en="Soups", slug="soups", description_uz="Milliy va yevropa suyuq taomlari", description_ru="Национальные и европейские супы", description_en="National and European soups", display_order=3, is_active=True)
            c4 = Category(id=4, name_uz="Salatlar", name_ru="Салаты", name_en="Salads", slug="salads", description_uz="Yangi sabzavotli salatlar", description_ru="Свежие овощные салаты", description_en="Fresh vegetable salads", display_order=4, is_active=True)
            c5 = Category(id=5, name_uz="Ichimliklar", name_ru="Напитки", name_en="Drinks", slug="drinks", description_uz="Issiq va sovuq ichimliklar", description_ru="Горячие и холодные напитки", description_en="Hot and cold drinks", display_order=5, is_active=True)
            session.add_all([c1, c2, c3, c4, c5])
            await session.commit()
            print("Kategoriyalar muvaffaqiyatli yuklandi.")
        else:
            print("Kategoriyalar allaqachon mavjud.")

        # 2. Add menu items if they don't exist
        res_items = await session.execute(select(MenuItem))
        menu_items = res_items.scalars().all()
        if not menu_items:
            m1 = MenuItem(
                category_id=1,
                name_uz="Toshkent Oshi (Palov)",
                name_ru="Ташкентский Плов",
                name_en="Tashkent Plav",
                description_uz="Zafarli to'y oshi. Qo'y go'shti, bedana tuxumi, kishmish va noxot bilan.",
                description_ru="Праздничный плов с бараниной, перепелиными яйцами, изюмом и нутом.",
                description_en="Traditional festive plav with tender lamb, quail eggs, raisins, and chickpeas.",
                price=45000,
                is_available=True,
                is_featured=True,
                image_url="https://images.unsplash.com/photo-1633945274405-b6c8069047b0?auto=format&fit=crop&w=600&q=80"
            )
            m2 = MenuItem(
                category_id=1,
                name_uz="Tuxum Barak",
                name_ru="Тухум Барак",
                name_en="Tukhum Barak",
                description_uz="Xorazmcha tuxumli chuchvara. Sariq sariyog' bilan birga tortiladi.",
                description_ru="Хорезмские пельмени с начинкой из яиц. Подается с топленым маслом.",
                description_en="Khorezmian style dumplings filled with egg, served with melted butter.",
                price=32000,
                is_available=True,
                is_featured=False,
                image_url="https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80"
            )
            m3 = MenuItem(
                category_id=2,
                name_uz="Qo'y Go'shtidan Shaurma Kabob",
                name_ru="Шашлык из баранины",
                name_en="Lamb Kebab",
                description_uz="Ko'mirda pishirilgan yumshoq va sershira shashlik, piyoz va limon bilan.",
                description_ru="Сочный и нежный шашлык из баранины на углях, с луком и лимоном.",
                description_en="Juicy lamb skewers grilled over charcoal, served with onions and lemon slices.",
                price=18000,
                is_available=True,
                is_featured=True,
                image_url="https://images.unsplash.com/photo-1555939594-58d7cb561ad1?auto=format&fit=crop&w=600&q=80"
            )
            m4 = MenuItem(
                category_id=2,
                name_uz="Mol Go'shtidan Qiymali Kabob",
                name_ru="Люля Кебаб",
                name_en="Lula Kebab",
                description_uz="Mol go'shtidan qiyma shashlik. Ko'mirning o'ziga xos hidi bilan.",
                description_ru="Люля-кебаб из говяжьего фарша со специями, приготовленный на углях.",
                description_en="Minced beef kebab with special oriental spices, grilled on hot coals.",
                price=15000,
                is_available=True,
                is_featured=False,
                image_url="https://images.unsplash.com/photo-1603360946369-dc9bb6258143?auto=format&fit=crop&w=600&q=80"
            )
            m5 = MenuItem(
                category_id=3,
                name_uz="Mastava",
                name_ru="Мастава",
                name_en="Mastava",
                description_uz="Go'sht va sabzavotlarga boy, qatiq bilan tortiladigan milliy guruchli sho'rva.",
                description_ru="Густой национальный рисовый суп с говядиной и овощами, подается со сметаной.",
                description_en="Rich national rice soup with beef and diced vegetables, served with sour cream.",
                price=24000,
                is_available=True,
                is_featured=False,
                image_url="https://images.unsplash.com/photo-1547592180-85f173990554?auto=format&fit=crop&w=600&q=80"
            )
            m6 = MenuItem(
                category_id=3,
                name_uz="Sho'rva (Qo'y go'shti bilan)",
                name_ru="Шурпа с бараниной",
                name_en="Traditional Shurpa",
                description_uz="Qo'y go'shti, noxot va sabzavotlar bilan pishirilgan tiniq va shifobaxsh sho'rva.",
                description_ru="Сытный суп с кусками баранины, нутом, картофелем и морковью.",
                description_en="Clear and nourishing lamb soup with chickpeas, potatoes, and carrots.",
                price=28000,
                is_available=True,
                is_featured=True,
                image_url="https://images.unsplash.com/photo-1607532941433-304659e8198a?auto=format&fit=crop&w=600&q=80"
            )
            m7 = MenuItem(
                category_id=4,
                name_uz="Achchiq-Chuchuq Salati",
                name_ru="Салат Ачик-Чучук",
                name_en="Achichuk Salad",
                description_uz="Yangi pomidor, piyoz va achchiq qalampirdan tayyorlangan milliy salat.",
                description_ru="Традиционный салат из спелых помидоров, тонко нарезанного лука и перца.",
                description_en="Traditional salad with ripe tomatoes, thinly sliced onions, and chili.",
                price=12000,
                is_available=True,
                is_featured=False,
                image_url="https://images.unsplash.com/photo-1512621776951-a57141f2eefd?auto=format&fit=crop&w=600&q=80"
            )
            m8 = MenuItem(
                category_id=5,
                name_uz="Limonli Ko'k Choy",
                name_ru="Зеленый чай с лимоном",
                name_en="Green Tea with Lemon",
                description_uz="Miyona sarxush qiluvchi limon bo'laklari bilan o'zbekona ko'k choy.",
                description_ru="Тонизирующий зеленый чай со свежими дольками лимона.",
                description_en="Refreshing traditional green tea served with fresh lemon slices.",
                price=6000,
                is_available=True,
                is_featured=False,
                image_url="https://images.unsplash.com/photo-1597481499750-3e6b22637e12?auto=format&fit=crop&w=600&q=80"
            )
            session.add_all([m1, m2, m3, m4, m5, m6, m7, m8])
            await session.commit()
            print("Taomlar muvaffaqiyatli yuklandi.")
        else:
            print("Taomlar allaqachon mavjud.")

        # 3. Add mock reservations if they don't exist
        res_booking = await session.execute(select(Reservation))
        bookings = res_booking.scalars().all()
        if not bookings:
            r1 = Reservation(
                guest_name="Shaxzod Alimov",
                phone="+998901234567",
                email="shaxzod@example.com",
                date=date(2026, 6, 26),
                time=time(18, 0),
                guests_count=4,
                special_requests="Deraza yonidan stol bo'lsin",
                status="confirmed"
            )
            r2 = Reservation(
                guest_name="Dilnoza Karimova",
                phone="+998935552211",
                email="dilnoza@example.com",
                date=date(2026, 6, 27),
                time=time(19, 30),
                guests_count=2,
                status="pending"
            )
            r3 = Reservation(
                guest_name="Bobur Mansurov",
                phone="+998978887766",
                date=date(2026, 6, 26),
                time=time(20, 0),
                guests_count=6,
                status="pending"
            )
            session.add_all([r1, r2, r3])
            await session.commit()
            print("Rezervatsiyalar muvaffaqiyatli yuklandi.")
        else:
            print("Rezervatsiyalar allaqachon mavjud.")

        # 4. Add mock messages if they don't exist
        res_msg = await session.execute(select(Contact))
        messages = res_msg.scalars().all()
        if not messages:
            msg1 = Contact(
                name="Jasur Komilov",
                email="jasur@gmail.com",
                subject="Hamkorlik taklifi",
                message="Assalomu alaykum, restoraningiz bilan hamkorlik qilish bo'yicha taklifimiz bor edi.",
                is_read=False
            )
            msg2 = Contact(
                name="Malika Ahmedova",
                email="malika@mail.ru",
                subject="Rahmat",
                message="Kechagi tug'ilgan kun tadbiri juda ajoyib o'tdi. Taomlar uchun katta rahmat!",
                is_read=True
            )
            session.add_all([msg1, msg2])
            await session.commit()
            print("Xabarlar muvaffaqiyatli yuklandi!")
        else:
            print("Xabarlar allaqachon mavjud.")

        print("Seed ishlari yakunlandi!")

if __name__ == "__main__":
    asyncio.run(seed())
