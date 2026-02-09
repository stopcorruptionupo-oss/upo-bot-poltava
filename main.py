import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ З РОЗШИРЕНИМИ ТЕКСТАМИ ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Оберіть тип «Щорічна» та звітний період «2025 рік».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Wiki НАЗК: Види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Ваші персональні дані: ПІБ, РНОКПП, УНЗР (обов'язково з ID-картки), адреса реєстрації та проживання, посада станом на 31.12.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Wiki НАЗК: Дані суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "1. Подружжя (навіть якщо проживаєте окремо, але в шлюбі).\n"
             "2. Діти до 18 років (незалежно від місця проживання).\n"
             "3. Співмешканці (спільний побут > 183 дні або на 31.12).\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Wiki НАЗК: Склад сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Об'єкти нерухомості</b>\n\n"
           "⚠️ <b>Вказуємо майно суб'єкта ТА членів сім'ї.</b>\n"
           "Власність, оренда, право користування (в т.ч. реєстрація місця проживання). Обов'язково вкажіть житло, де ви жили на 31.12.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Wiki НАЗК: Нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Об'єкти (ваші або сім'ї), не прийняті в експлуатацію, або де не зареєстровано право власності.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Wiki НАЗК: Будівництво</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Ювелірні вироби, техніка, антикваріат (якщо вартість одиниці > 100 ПМ). Транспорт сюди НЕ входить.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Wiki НАЗК: Цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "⚠️ <b>Вказуємо транспорт суб'єкта ТА членів сім'ї.</b>\n"
           "Авто, мотоцикли, причепи у власності чи користуванні (хоча б 1 день).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Wiki НАЗК: Транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації, що належать вам або членам сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Wiki НАЗК: Цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "Частки у статутному капіталі підприємств (ТОВ), що належать вам або сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Wiki НАЗК: Корпоративні права</a>"),

    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Юридичні особи, над якими ви або сім'я здійснюєте контроль через третіх осіб.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Wiki НАЗК: Бенефіціари</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "Криптовалюти, патенти, торгові марки. Криптовалюта вказується як 'Нематеріальний актив'.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Wiki НАЗК: Активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "⚠️ <b>Обов'язково вказуємо доходи УСІХ членів сім'ї.</b>\n"
            "Зарплата (брутто), пенсія, допомога ВПО, відсотки в банку, подарунки.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Wiki НАЗК: Доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "⚠️ <b>Готівка та рахунки суб'єкта ТА сім'ї.</b>\n"
            "Декларується, якщо сумарно (ви + сім'я) > 50 ПМ (понад 151 400 грн).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Wiki НАЗК: Гроші</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські рахунки</b>\n\n"
              "Усі відкриті рахунки (IBAN) ваші та сім'ї за звітний рік, навіть якщо там 0 грн.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Wiki НАЗК: Рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, позики, ліміти по картках (ваші та сім'ї), якщо борг на 31.12 > 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Wiki НАЗК: Кредити</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Тільки разові витрати СУБ'ЄКТА (ваші особисті) понад 50 ПМ за один чек.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Wiki НАЗК: Видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "🚫 Поліцейським заборонено (крім викладання, науки, творчості чи медицини).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Wiki НАЗК: Сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Членство в керівних чи наглядових органах ГО, фондів, кооперативів.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Wiki НАЗК: Організації</a>")
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

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до <b>31 березня 2026 року включно</b>.", parse_mode="HTML")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Альона</b>\n📞 <code>0660787241</code>", parse_mode="HTML")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ <b>Відповідальність:</b>\n• Адміністративна (штрафи)\n• Дисциплінарна (звільнення)\n• Кримінальна (за недостовірні дані).", parse_mode="HTML")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу для довідки:", reply_markup=sections_menu(), parse_mode="HTML")

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
