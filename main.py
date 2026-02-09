import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
# Використовуємо ваш останній робочий токен
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ (З ОНОВЛЕНИМИ РОЗДІЛАМИ) ---
ANSWERS = {
    "Р1": "👤 **Розділ 1: Вид декларації**\nОберіть «Щорічна» та звітний період 2025 рік.",
    "Р2": "👥 **Розділ 2: Члени сім’ї**\nЧоловік/дружина, діти до 18 років, та особи, що спільно проживають понад 183 дні.",
    "Р2.1": "🪪 **Розділ 2.1: Склад сім'ї (Детально)**\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Офіційне роз'яснення НАЗК</a>",
    "Р3": "🏠 **Розділ 3: Нерухомість**\nВласність, оренда та обов'язково право користування за місцем прописки.",
    "Р4": "💎 **Розділ 4: Цінне майно**\nРечі вартістю понад 100 ПМ (крім авто).",
    "Р5": "🏗️ **Розділ 5: Незавершене будівництво**\nОб’єкти, не прийняті в експлуатацію.",
    "Р6": "🚗 **Розділ 6: Транспорт**\nУсі ТЗ, якими володіли або користувалися хоча б 1 день.",
    "Р7": "📈 **Розділ 7: Цінні папери**\nАкції, облігації тощо.",
    "Р8": "🏢 **Розділ 8: Корпоративні права**\n⚠️ Для поліцейських діють обмеження щодо управління.",
    "Р9": "👤 **Розділ 9: Бенефіціарна власність**\nКонтроль над юридичними особами.",
    "Р10": "💡 **Розділ 10: Нематеріальні активи**\nКриптовалюти, патенти, програми.",
    "Р11": "💰 **Розділ 11: Доходи та подарунки**\nЗарплата (БРУТТО), пенсія, допомога ВПО, подарунки.",
    "Р12": "💵 **Розділ 12: Грошові активи**\nГотівка та кошти на картках (якщо сукупно > 50 ПМ).",
    
    # ОНОВЛЕНІ РОЗДІЛИ ТУТ:
    "Р12.1": "💳 **Розділ 12.1: Банківські рахунки**\nВказуються всі номери рахунків (IBAN), відкриті на ваше ім'я або ім'я членів сім'ї протягом звітного періоду, навіть якщо вони порожні або закриті.\n🔗 [Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/)",
    
    "Р13": "📉 **Розділ 13: Фінансові зобов’язання**\nОтримані кредити, позики, залишки за кредитними картками. Вказуємо, якщо борг на кінець року > 50 ПМ.\n🔗 [Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/)",
    
    "Р14": "🧾 **Розділ 14: Видатки та правочини**\nВказуються тільки разові видатки СУБ'ЄКТА декларування, сума яких перевищує 50 ПМ.\n🔗 [Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/)",
    
    "Р15": "⚠️ **Розділ 15: Робота за сумісництвом**\n🚫 Поліцейським ЗАБОРОНЕНО займатися іншою оплачуваною діяльністю (ст. 25 Закону).\nДозволено лише викладацьку, наукову, творчу чи медпрактику.\n🔗 [Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/)",
    
    "Р16": "🏛️ **Розділ 16: Членство в організаціях**\nВходження до керівних, ревізійних чи наглядових органів громадських організацій, фондів чи кооперативів.\n🔗 [Wiki НАЗК](https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/)"
}

# --- МЕНЮ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни"), types.KeyboardButton(text="📂 Розділи декларації"))
    builder.row(types.KeyboardButton(text="📞 Зв'язок з адміном"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    # Створюємо кнопки для розділів 1-12
    for i in range(1, 13):
        builder.add(types.KeyboardButton(text=f"Розділ {i}"))
    
    # Додаємо специфічні розділи, які ви просили
    builder.add(types.KeyboardButton(text="Розділ 12.1"))
    builder.add(types.KeyboardButton(text="Розділ 13"))
    builder.add(types.KeyboardButton(text="Розділ 14"))
    builder.add(types.KeyboardButton(text="Розділ 15"))
    builder.add(types.KeyboardButton(text="Розділ 16"))
    builder.add(types.KeyboardButton(text="Розділ 2.1"))
    
    builder.adjust(4) # По 4 кнопки в ряд
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("✅ Вітаю! Я оновлений бот-помічник УПО Полтавщини.\nОберіть пункт:", reply_markup=main_menu())

@dp.message(F.text == "📅 Терміни")
async def terms(message: types.Message):
    await message.answer("📅 **Щорічна декларація за 2025 рік** подається до 31 березня 2026 року.")

@dp.message(F.text == "📂 Розділи декларації")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu())

@dp.message(F.text == "📞 Зв'язок з адміном")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Альона:**\n📞 +380660787241")

@dp.message(F.text == "⬅️ Назад")
async def go_back(message: types.Message):
    await message.answer("Головне меню:", reply_markup=main_menu())

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], parse_mode="Markdown", disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling
