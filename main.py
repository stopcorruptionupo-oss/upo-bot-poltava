import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
# Токен бота для УПО Полтавської області
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- БАЗА ЗНАНЬ (УСІ РОЗДІЛІВ ОКРЕМО З ПОСИЛАННЯМИ) ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\nОберіть тип «Щорічна» та звітний період «2025 рік».\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Інструкція НАЗК</a>"),
    
    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\nВаші дані: ПІБ, РНОКПП, УНЗР.\n🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>.\n🏷 Код ЄДРПОУ: <b>40109042</b>.\n⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обов'язково обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Інструкція НАЗК</a>"),
    
    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\nВписуємо подружжя, дітей до 18 років та осіб, що спільно проживали > 183 дні протягом року.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Інструкція НАЗК</a>"),
    
    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n⚠️ <b>Вказуємо майно суб'єкта ТА сім'ї.</b> Власність, оренда, право користування (прописка). Обов'язково вкажіть об'єкт, де ви або сім'я фактично перебували на 31.12.2025.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Інструкція НАЗК</a>"),
    
    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Інструкція НАЗК</a>"),
    
    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Інструкція НАЗК</a>"),
    
    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n⚠️ <b>Ваші авто та авто сім'ї.</b> Вказуємо власність, користування, техпаспорт або довіреність.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Інструкція НАЗК</a>"),
    
    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Інструкція НАЗК</a>"),
    
    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n⚠️ <b>ДЛЯ ПОЛІЦЕЙСЬКИХ:</b> Заборонено мати частки в прибуткових фірмах (ТОВ, ПП). Якщо такі права є, вони мали бути передані в управління.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Інструкція НАЗК</a>"),
    
    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Інструкція НАЗК</a>"),
    
    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n🟡 <b>Криптовалюти:</b> Назва монети, кількість, дата набуття, біржа або ідентифікатор гаманця.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Інструкція НАЗК</a>"),
    
    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n⚠️ <b>Обов'язково доходи УСІЄЇ СІМ'Ї.</b> Зарплата (брутто), пенсія, допомога ВПО, аліменти, відсотки.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Інструкція НАЗК</a>"),
    
    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Інструкція НАЗК</a>"),
    
    "Р12.1": ("💳 <b>Розділ 12.1: Банківські установи</b>\n\n⚠️ <b>ТІЛЬКИ НАЗВИ БАНКІВ:</b> Обираємо назви банків (Приват, Ощад, Монобанк тощо), де відкрито рахунки у вас або сім'ї. IBAN писати НЕ потрібно.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Інструкція НАЗК</a>"),
    
    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Інструкція НАЗК</a>"),
    
    "Р14": "🧾 <b>Розділ 14: Видатки та правочини</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Інструкція НАЗК</a>",
    "Р15": "⚠️ <b>Розділ 15: Сумісництво</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Інструкція НАЗК</a>",
    "Р16": "🏛️ <b>Розділ 16: Членство в організаціях</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Інструкція НАЗК</a>"
}

# --- КЛАВІАТУРИ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📥 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="🔍 Автоперевірка своєї декларації"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="👤 Адміністратор"), types.KeyboardButton(text="⚖️ Відповідальність"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    btns = ["Розділ 1", "Розділ 2", "Розділ 2.1", "Розділ 3", "Розділ 4", "Розділ 5", 
            "Розділ 6", "Розділ 7", "Розділ 8", "Розділ 9", "Розділ 10", "Розділ 11", 
            "Розділ 12", "Розділ 12.1", "Розділ 13", "Розділ 14", "Розділ 15", "Розділ 16"]
    for b in btns:
        builder.add(types.KeyboardButton(text=b))
    builder.adjust(3)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 <b>Головне меню Полтавського УПО</b>. Оберіть потрібний розділ:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "📥 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer(
        "📥 <b>Автозаповнення декларації</b>\n\nСкористайтеся інструкцією за посиланням:\n"
        "🔗 <a href='
