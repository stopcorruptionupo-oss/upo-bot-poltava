

import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# ВАШ НОВИЙ ТОКЕН ВЖЕ ТУТ
TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функція для створення головного меню
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

# Команда /start
@dp.message(F.text == "/start")
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 <b>Бот оновлено!</b>\n\nТепер тут доступні всі розділи декларації (1-16).\n"
        "Оберіть потрібний розділ для отримання довідки:",
        reply_markup=get_keyboard(),
        parse_mode=ParseMode.HTML
    )

# Обробник повідомлень (тексти розділів)
@dp.message()
async def handle_message(message: types.Message):
    t = message.text
    
    if t == "Розділ 1-2. Сім'я":
        await message.answer("<b>Розділ 1-2. Суб'єкт та сім'я</b>\nДекларуємо себе, чоловіка/дружину та дітей.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iv-sub-yekt-deklaruvannya-ta-chleny-jogo-sim-yi/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)
    
    elif t == "Розділ 2.1. Об'єкти сім'ї":
        await message.answer("<b>Розділ 2.1. Відомості про об’єкти сім'ї</b>\nЗаповнюється, якщо член сім'ї не надав дані про своє майно.", parse_mode=ParseMode.HTML)
        
    elif t == "Розділ 3. Нерухомість":
        await message.answer("<b>Розділ 3. Нерухомість</b>\nВласність, оренда, користування.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)

    elif t == "Розділ 4. Цінні речі":
        await message.answer("<b>Розділ 4. Цінні речі</b>\nМайно вартістю понад 100 ПМ (крім авто).\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-tsinne-ruhome-majno/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)

    elif t == "Розділ 6. Транспорт":
        await message.answer("<b>Розділ 6. Транспорт</b>\nАвто, мотоцикли, причепи.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-tsinne-ruhome-majno-transportni-zasoby/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)

    elif t == "Розділ 11. Доходи":
        await message.answer("<b>Розділ 11. Доходи</b>\nЗарплата, подарунки, допомога ВПО.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xiii-dohody-u-tomu-chysli-podarunky/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)

    elif t == "Розділ 12.1. Рахунки":
        await message.answer("<b>Розділ 12.1. Банківські рахунки</b>\nУсі IBAN-рахунки (навіть порожні).\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Роз'яснення НАЗК</a>", parse_mode=ParseMode.HTML)

    elif t == "Розділ 15. Сумісництво":
        await message.answer("<b>Розділ 15. Сумісництво</b>\n🚫 Поліцейським заборонено оплачувану роботу (крім викладацької).\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/'>Детальніше</a>", parse_mode=ParseMode.HTML)
    
    else:
        await message.answer("Будь ласка, оберіть розділ з меню.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
