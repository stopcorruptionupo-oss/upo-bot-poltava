import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode

# ВАШ ТОКЕН ВЖЕ ТУТ
TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoA1rlcaGXpTs8Qt4"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Кнопки меню
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
        "👋 Бот відновлено! Оберіть розділ декларації для отримання довідки та посилання:",
        reply_markup=get_keyboard()
    )

# Універсальний обробник
@dp.message()
async def handle_docs(message: types.Message):
    responses = {
        "Розділ 1-2. Сім'я": "<b>Розділ 1-2</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iv-sub-yekt-deklaruvannya-ta-chleny-jogo-sim-yi/'>НАЗК</a>",
        "Розділ 12.1. Рахунки": "<b>Розділ 12.1. Рахунки</b>\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>НАЗК</a>",
        "Розділ 15. Сумісництво": "<b>Розділ 15. Сумісництво</b>\n🚫 Поліцейським заборонено ст. 25 Закону!\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/'>Детальніше</a>"
    }
    
    text = responses.get(message.text, "Оберіть розділ з меню або напишіть /start")
    await message.answer(text, parse_mode=ParseMode.HTML)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
