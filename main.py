import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
# Ваш актуальний токен
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- БАЗА ЗНАНЬ (ПОВНІ ТЕКСТИ) ---
ANSWERS = {
    "Р1": "📋 **Розділ 1: Вид декларації**\nОберіть тип «Щорічна» та звітний період «2025 рік».",
    
    "Р2": "👤 **Розділ 2: Суб'єкт декларування**\nТут вказуються ВАШІ персональні дані: ПІБ, РНОКПП, УНЗР, адреса реєстрації та фактичного проживання, місце роботи, посада та категорія посади.",
    
    "Р2.1": "👥 **Розділ 2.1: Члени сім'ї суб'єкта декларування**\nВказуються: чоловік/дружина, діти до 18 років (незалежно від проживання) та особи, які спільно проживали > 183 днів на рік або станом на 31.12.\n🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Детально на Wiki НАЗК</a>",
    
    "Р3": "🏠 **Розділ 3: Об'єкти нерухомості**\nВласність, оренда, право користування (в т.ч. реєстрація місця проживання). Не забудьте вказати об'єкт, де ви жили на 31.12.",
    
    "Р4": "🏗️ **Розділ 4: Об'єкти незавершеного будівництва**\nНедобудоване майно, не прийняте в експлуатацію або не зареєстроване в реєстрі.",
    
    "Р5": "💎 **Розділ 5: Цінне рухоме майно**\nЮвелірні вироби, техніка, антикваріат (якщо ціна одного предмета > 100 ПМ).",
    
    "Р6": "🚗 **Розділ 6: Транспортні засоби**\nВсі авто, якими ви чи сім'я володіли або користувалися протягом року (навіть 1 день).",
    
    "Р12.1": "💳 **Розділ 12.1: Банківські рахунки**\nВказуються всі номери рахунків (IBAN) ваші та сім'ї, відкриті у звітному році (навіть якщо вони вже закриті або порожні).",
    
    "Р13": "📉 **Розділ 13: Фінансові зобов’язання**\nКредити, позики, ліміти по картках. Вказуємо, якщо борг на кінець року перевищує 50 ПМ.",
    
    "Р14": "🧾 **Розділ 14: Видатки та правочини**\nТільки разові витрати СУБ'ЄКТА (ваші особисті) понад 50 ПМ.",
    
    "Р15": "⚠️ **Розділ 15: Робота за сумісництвом**\n🚫 Поліцейським заборонено іншу оплачувану діяльність, крім викладацької, наукової чи творчої.",
    
    "Р16": "🏛️ **Розділ 16: Членство в організаціях**\nВходження до керівних, ревізійних чи наглядових органів ГО, фондів, кооперативів."
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
    # Нумерація за формою НАЗК
    builder.add(types.KeyboardButton(text="Розділ 1"))
    builder.add(types.KeyboardButton(text="Розділ 2"))
    builder.add(types.KeyboardButton(text="Розділ 2.1"))
    builder.add(types.KeyboardButton(text="Розділ 3"))
    builder.add(types.KeyboardButton(text="Розділ 4"))
    builder.add(types.KeyboardButton(text="Розділ 5"))
    builder.add(types.KeyboardButton(text="Розділ 6"))
    builder.add(types.KeyboardButton(text="Розділ 12.1"))
    builder.add(types.KeyboardButton(text="Розділ 13"))
    builder.add(types.KeyboardButton(text="Розділ 14"))
    builder.add(types.KeyboardButton(text="Розділ 15"))
    builder.add(types.KeyboardButton(text="Розділ 16"))
    
    builder.adjust(3) # По 3 кнопки в ряд
    builder.row(types.KeyboardButton(text="⬅️ Назад"))
    return builder.as_markup(resize_keyboard=True)

# --- ОБРОБНИКИ ---

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 **Головне меню**. Оберіть потрібний блок інформації:", reply_markup=main_menu())

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 **Щорічна декларація за 2025 рік** подається з 1 січня по **31 березня 2026 року включно**.")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 **Адміністратор Альона**\n📞 Номер телефону: `0660787241`\nЗвертайтесь за допомогою у робочий час.")

@dp.message(F.text == "⚖️ Відповідальність")
async def responsibility(message: types.Message):
    await message.answer("⚖️ **Відповідальність:**\n\n• **Адміністративна:** за несвоєчасне подання (штрафи).\n• **Дисциплінарна:** звільнення з органів НПУ.\n• **Кримінальна:** за недостовірні відомості (якщо різниця > 1.5 млн грн).")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу (як у формі НАЗК) для довідки:", reply_markup=sections_menu())

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
