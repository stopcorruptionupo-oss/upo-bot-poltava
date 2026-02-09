import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# Отримання токена (Render автоматично підтягне його з Environment Variables)
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Створення меню (кнопки розділів)
def get_keyboard():
    buttons = [
        [KeyboardButton(text="Розділ 1-2. Сім'я"), KeyboardButton(text="Розділ 2.1. Об'єкти сім'ї")],
        [KeyboardButton(text="Розділ 3. Нерухомість"), KeyboardButton(text="Розділ 4. Цінні речі")],
        [KeyboardButton(text="Розділ 5. Будівництво"), KeyboardButton(text="Розділ 6. Транспорт")],
        [KeyboardButton(text="Розділ 7-10. Активи"), KeyboardButton(text="Розділ 11. Доходи")],
        [KeyboardButton(text="Розділ 12. Гроші"), KeyboardButton(text="Розділ 12.1. Рахунки")],
        [KeyboardButton(text="Розділ 13. Кредити"), KeyboardButton(text="Розділ 14. Видатки")],
        [KeyboardButton(text="Розділ 15. Сумісництво"), KeyboardButton(text="Розділ 16. Органи")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "<b>Довідник з декларування (2025-2026)</b>\n\n"
        "Оберіть розділ декларації, щоб отримати коротку довідку та офіційне посилання на роз'яснення НАЗК.",
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.HTML
    )

# --- ОБРОБНИКИ ВСІХ РОЗДІЛІВ ---

@dp.message(F.text == "Розділ 1-2. Сім'я")
async def sec_1_2(message: types.Message):
    await message.answer(
        "<b>Розділ 1 та 2. Суб'єкт та члени сім'ї</b>\n\n"
        "• Перевірте ПІБ, РНОКПП та адресу.\n"
        "• Члени сім'ї: чоловік/дружина, діти до 18 років, та особи, що спільно проживають більше 183 днів.\n\n"
        "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iv-sub-yekt-deklaruvannya-ta-chleny-jogo-sim-yi/'>Роз'яснення НАЗК</a>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "Розділ 2.1. Об'єкти сім'ї")
async def sec_2_1(message: types.Message):
    await message.answer(
        "<b>Розділ 2.1. Відомості про об’єкти членів сім'ї</b>\n\n"
        "Заповнюється, якщо член сім'ї відмовився надати дані про своє майно.\n\n"
        "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/'>База знань НАЗК</a>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "Розділ 3. Нерухомість")
async def sec_3(message: types.Message):
    await message.answer(
        "<b>Розділ 3. Нерухомість</b>\n\n"
        "• Декларується власність, оренда та користування (навіть 'прописка').\n"
        "• Обов'язково вказуйте об'єкт, у якому ви проживали на 31.12.\n\n"
        "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Роз'яснення НАЗК</a>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "Розділ 4. Цінні речі")
async def sec_4(message: types.Message):
    await message.answer(
        "<b>Розділ 4. Цінне рухоме майно</b>\n\n"
        "Ювелірні вироби, годинники, антикваріат, якщо вартість перевищує 100 прожиткових мінімумів.\n\n"
        "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-tsinne-ruhome-majno/'>Роз'яснення НАЗК</a>",
        parse_mode=ParseMode.HTML
    )

@dp.message(F.text == "Розділ 5. Будівництво")
async def sec_5(message: types.Message):
    await message.answer
