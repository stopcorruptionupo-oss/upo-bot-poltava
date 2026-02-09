import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ (УСІ РОЗДІЛИ) ---
ANSWERS = {
    "Р1": "📋 **Розділ 1: Вид декларації**\nОберіть тип «Щорічна» та звітний період «2025 рік».",
    "Р2": "👤 **Розділ 2: Суб'єкт декларування**\nВаші дані: ПІБ, РНОКПП, УНЗР, місце роботи та посада.",
    "Р2.1": "👥 **Розділ 2.1: Члени сім'ї**\nЧоловік/дружина, діти до 18 років та особи, що спільно проживають > 183 днів.",
    "Р3": "🏠 **Розділ 3: Об'єкти нерухомості**\nВласність, оренда та право користування (прописка).",
    "Р4": "🏗️ **Розділ 4: Незавершене будівництво**\nНедобудовані або не зареєстровані об'єкти.",
    "Р5": "💎 **Розділ 5: Цінне рухоме майно**\nРечі дорожче 100 ПМ (ювелірні вироби, техніка).",
    "Р6": "🚗 **Розділ 6: Транспортні засоби**\nВсі авто у власності чи користуванні (навіть 1 день).",
    "Р7": "📈 **Розділ 7: Цінні папери**\nАкції, облігації, що належать вам або сім'ї.",
    "Р8": "🏢 **Розділ 8: Корпоративні права**\nЧастки у статутному капіталі товариств/підприємств.",
    "Р9": "👤 **Розділ 9: Юридичні особи (бенефіціар)**\nКомпанії, де ви або сім'я є кінцевими власниками.",
    "Р10": "💡 **Розділ 10: Нематеріальні активи**\nКриптовалюти, патенти, торгові марки.",
    "Р11": "💰 **Розділ 11: Доходи та подарунки**\nЗарплата (брутто), пенсія, допомога ВПО, подарунки.",
    "Р12": "💵 **Розділ 12: Грошові активи**\nГотівка та кошти на картках (якщо сукупно > 50 ПМ).",
    "Р12.1": "💳 **Розділ 12.1: Банківські рахунки**\nВсі номери IBAN, відкриті протягом року.",
    "Р13": "📉 **Розділ 13: Фінансові зобов’язання**\nКредити, позики, ліміти карт (борг > 50 ПМ).",
    "Р14": "🧾 **Розділ 14: Видатки та правочини**\nРазові витрати суб'єкта понад 50 ПМ.",
    "Р15": "⚠️ **Розділ 15: Робота за сумісництвом**\n🚫 Заборонено (крім викладацької, наукової, творчої).",
    "Р16": "🏛️ **Розділ 16: Членство в організаціях**\nКерівні органи ГО, фондів."
}

# --- МЕНЮ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="👤 Адмін"), types.KeyboardButton(text="⚖️ Відповідальність"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    return builder.as_markup(resize_keyboard=True)

def sections_menu():
    builder = ReplyKeyboardBuilder()
    # Додаємо всі кнопки по порядку
    buttons = [
        "Розділ 1", "Розділ 2", "Розділ 2.1", "Розділ 3",
        "Розділ 4", "Розділ 5", "Розділ 6", "Розділ 7",
        "Розділ 8", "Розділ 9", "Розділ 10", "Розділ 11",
        "Розділ 12", "Розділ 12.1", "Розділ 13", "Розділ 14",
        "Розділ 15", "Розділ 16"
    ]
    for btn_text in buttons:
        builder.add(types.KeyboardButton(text=btn_text))
    
    builder.adjust(3)
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 **Головне меню**. Оберіть потрібний блок:", reply_markup=main_menu())

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 **Щорічна декларація за 2025 рік** подається до **31 березня 2026 року включно**.")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Альона**\n📞 Номер телефону: `0660787241`")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ **Відповідальність:** Адміністративна (штрафи), Дисциплінарна (звільнення), Кримінальна (за брехню у великих розмірах).")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу:", reply_markup=sections_menu())

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
