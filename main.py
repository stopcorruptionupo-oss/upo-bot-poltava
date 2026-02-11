import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- МАКСИМАЛЬНО РОЗШИРЕНА БАЗА ЗНАНЬ (УСІ РОЗДІЛИ З ПОСИЛАННЯМИ) ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Обираємо тип «Щорічна» та звітний період «2025 рік».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Інструкція: Види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Ваші дані: ПІБ, РНОКПП, УНЗР (13 цифр з ID-картки).\n"
           "🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>.\n"
           "🏷 Код ЄДРПОУ: <b>40109042</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обов'язково обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Інструкція: Дані суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Вписуємо подружжя, дітей до 18 років та осіб, що спільно проживали понад 183 дні протягом року.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Інструкція: Склад сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n"
           "⚠️ <b>Вказуємо майно суб'єкта ТА членів сім'ї.</b>\n"
           "Власність, оренда, право користування (прописка). Обов'язково вкажіть об'єкт, де ви або сім'я фактично перебували на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Інструкція: Нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Недобудоване майно або об'єкти без офіційної реєстрації права власності.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Інструкція: Будівництво</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Ювелірні вироби, техніка (якщо вартість > 100 ПМ). Авто сюди НЕ входить.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Інструкція: Цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Вказуємо транспорт суб'єкта ТА членів сім'ї. Власність, користування по техпаспорту чи довіреності.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Інструкція: Транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації (в т.ч. військові), що належать вам або родичам.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Інструкція: Цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "⚠️ <b>ДЛЯ ПОЛІЦЕЙСЬКИХ:</b> Заборонено входити до правління прибуткових фірм. "
           "Якщо ви маєте частку в ТОВ, вона повинна бути передана в управління (траст). Члени сім'ї декларують бізнес без обмежень.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Інструкція: Корп. права</a>"),

    "Р9": ("🏢 <b>Розділ 9: Юридичні особи (Бенефіціар)</b>\n\n"
           "Фірми, підконтрольні вам або сім'ї через посередників.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Інструкція: Бенефіціари</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "🟡 <b>Криптовалюти:</b> Назва (BTC, ETH), кількість монет, дата набуття, біржа/гаманець.\n"
            "🟡 <b>Авторські права:</b> Патенти, торгові марки.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Інструкція: Нематеріальні активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "<b>Ваші та ВСІХ членів сім'ї</b>. Зарплата (брутто), пенсія, допомога ВПО, відсотки, подарунки.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Інструкція: Доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка та гроші на картках (ваші + сім'ї). Декларується, якщо сумарно > 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Інструкція: Гроші</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські установи</b>\n\n"
              "<b>⚠️ ТІЛЬКИ НАЗВИ БАНКІВ:</b>\n"
              "Обираємо зі списку назви банків (Приват, Ощад, Монобанк тощо), де у вас або сім'ї відкриті рахунки.\n"
              "• Номери IBAN вписувати НЕ потрібно.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Інструкція: Рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, борги по лімітах (ваші та сім'ї), якщо сума на 31.12 > 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Інструкція: Кредити</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Разові витрати СУБ'ЄКТА понад 50 ПМ за один чек.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Інструкція: Видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "Заборонено (крім викладання, науки, творчості чи медицини).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Інструкція: Сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Участь у керівних органах ГО, фондів ваші або сім'ї.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Інструкція: Організації</a>")
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
    await message.answer("📝 Оберіть номер розділу для довідки:", reply_markup=sections_menu(), parse_mode="HTML")

@dp.message(F.text.startswith("Розділ "))
async def handle_section(message: types.Message):
    num = message.text.replace("Розділ ", "Р")
    if num in ANSWERS:
        await message.answer(ANSWERS[num], parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до 31 березня 2026 року включно.", parse_mode="HTML")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Альона</b>\n📞 <code>0660787241</code>", parse_mode="HTML")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ <b>Відповідальність:</b> Адмін, Дисциплінарна, Кримінальна.", parse_mode="HTML")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
