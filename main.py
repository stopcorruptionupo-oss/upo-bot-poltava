import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- МАКСИМАЛЬНО РОЗШИРЕНА БАЗА ЗНАНЬ (18 РОЗДІЛІВ) ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Оберіть тип «Щорічна» та звітний період «2025 рік»."),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Ваші дані: ПІБ, РНОКПП, УНЗР.\n"
           "🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>.\n"
           "🏷 Код ЄДРПОУ: <b>40109042</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обов'язково обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Wiki НАЗК</a>"),

    "Р2.1": "👥 <b>Розділ 2.1: Члени сім'ї</b>\nВписуємо подружжя, дітей до 18 років та осіб, що спільно проживають.",

    "Р3": "🏠 <b>Розділ 3: Нерухомість</b>\nВласність, оренда та право проживання (прописка) вас та сім'ї.",

    "Р4": "🏗️ <b>Розділ 4: Незавершене будівництво</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Wiki НАЗК</a>",
    "Р5": "💎 <b>Розділ 5: Цінне майно</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Wiki НАЗК</a>",
    "Р6": "🚗 <b>Розділ 6: Транспортні засоби</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Wiki НАЗК</a>",
    "Р7": "📈 <b>Розділ 7: Цінні папери</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Wiki НАЗК</a>",

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "⚠️ <b>ВАЖЛИВО ДЛЯ ПОЛІЦЕЙСЬКИХ:</b>\n"
           "Згідно зі ст. 25 Закону 'Про запобігання корупції', поліцейським <b>ЗАБОРОНЕНО</b> входити до складу органу управління чи наглядової ради підприємства, що має на меті одержання прибутку.\n\n"
           "✅ <b>Що робити, якщо у вас є частка в ТОВ?</b>\n"
           "Ви повинні були <b>передати ці права в управління</b> іншій особі протягом 60 днів після призначення на посаду. В декларації вони все одно вказуються, але з позначкою про передачу в управління.\n\n"
           "✅ <b>Члени сім'ї:</b>\n"
           "Для членів сім'ї (дружини/чоловіка) таких обмежень немає. Якщо бізнес записаний на них, ви просто вказуєте їхню частку в статутному капіталі тут.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Докладніше про Розділ 8</a>"),

    "Р9": "🏢 <b>Розділ 9: Бенефіціарна власність</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Wiki НАЗК</a>",

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "Криптовалюти (назва, кількість, біржа), авторські права та патенти.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Wiki НАЗК</a>"),

    "Р11": "💰 <b>Розділ 11: Доходи та подарунки</b>\nЗарплата (брутто), пенсія, допомога ВПО тощо.",

    "Р12": "💵 <b>Розділ 12: Грошові активи</b>\nГотівка та рахунки, якщо сукупно > 50 ПМ.",

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські та інші установи</b>\n\n"
              "<b>⚠️ ТІЛЬКИ НАЗВИ БАНКІВ:</b>\n"
              "Вказуємо назви банків (ПриватБанк, Ощадбанк тощо), де у вас або сім'ї відкриті рахунки.\n"
              "• Номери IBAN вписувати НЕ потрібно.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Wiki НАЗК</a>"),

    "Р13": "📉 <b>Розділ 13: Фінансові зобов’язання</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Wiki НАЗК</a>",
    "Р14": "🧾 <b>Розділ 14: Видатки та правочини</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Wiki НАЗК</a>",
    "Р15": "⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Wiki НАЗК</a>",
    "Р16": "🏛️ <b>Розділ 16: Членство в організаціях</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Wiki НАЗК</a>"
}

# --- КЛАВІАТУРИ ---
def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="👤 Адмін"), types.KeyboardButton(text="⚖️ Відповідальність"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
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
    await message.answer("📋 <b>Головне меню</b>. Оберіть пункт:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu(), parse_mode="HTML")

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], parse_mode="HTML", disable_web_page_preview=True)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
