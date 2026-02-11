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
           "Оберіть тип «Щорічна» та звітний період «2025 рік». "
           "Якщо ви подаєте декларацію вперше після призначення — «Кандидата на посаду». "
           "Якщо звільняєтесь — «При звільненні».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Інструкція НАЗК: Види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Ваші дані: ПІБ, РНОКПП, УНЗР (13 цифр з вашої ID-картки).\n"
           "🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>.\n"
           "🏷 Код ЄДРПОУ: <b>40109042</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n"
           "Вказуйте посаду, на якій ви працювали станом на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Інструкція НАЗК: Дані суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Сюди вписуємо: чоловіка/дружину (навіть якщо проживаєте окремо, але шлюб не розірвано), дітей до 18 років (незалежно від місця проживання) та осіб, що спільно проживають понад 183 дні.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Інструкція НАЗК: Склад сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n"
           "Декларуємо майно <b>ваше та сім'ї</b>. Власність, оренда, право проживання (прописка). "
           "Обов'язково вкажіть житло, де ви та сім'я фактично перебували на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Інструкція НАЗК: Нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Будинки, що будуються, або об'єкти, не прийняті в експлуатацію чи не зареєстровані в реєстрі нерухомості на вас чи сім'ю.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Інструкція НАЗК: Будівництво</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Речі (ювелірка, техніка, антикваріат), вартість яких перевищує 100 прожиткових мінімумів. Авто сюди не пишемо.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Інструкція НАЗК: Цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "<b>Ваші авто та авто сім'ї</b>. Вказуємо все: власність, користування по техпаспорту або довіреності, якщо користувалися хоча б 1 день.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Інструкція НАЗК: Транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації (в т.ч. військові), що належать вам або членам вашої сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Інструкція НАЗК: Цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "Частки у статутному капіталі фірм (ТОВ, ПП), де ви або сім'я є співвласниками.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Інструкція НАЗК: Корп. права</a>"),

    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Компанії, якими ви або сім'я володієте через посередників.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Інструкція НАЗК: Бенефіціари</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "Криптовалюти, авторські права, торгові марки. Крипту вказуємо обов'язково із зазначенням типу та кількості.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Інструкція НАЗК: Активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "<b>Ваші та ВСІХ членів сім'ї</b>. Зарплата (повна сума до вирахування податків), пенсія, соцвиплати, аліменти, відсотки, подарунки.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Інструкція НАЗК: Доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка та гроші на рахунках (ваші + сім'ї). Декларується, якщо сума перевищує 50 ПМ.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Інструкція НАЗК: Гроші</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські та інші установи</b>\n\n"
              "<b>⚠️ УВАГА! ЦЕЙ РОЗДІЛ ОБОВ'ЯЗКОВИЙ:</b>\n"
              "Потрібно вказати <b>УСІ РАХУНКИ (IBAN)</b>, відкриті на ваше ім'я та ім'я членів сім'ї протягом року.\n"
              "• Навіть якщо на рахунку 0 грн.\n"
              "• Навіть якщо рахунок був відкритий лише на 1 день і вже закритий.\n"
              "• Включаючи кредитні картки, 'монобанки', соціальні картки.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Інструкція НАЗК: Рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, позики, ліміти по картках (ваші та сім'ї). Пишемо, якщо борг > 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Інструкція НАЗК: Кредити</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Разові витрати <b>ТІЛЬКИ ВАШІ</b> понад 50 ПМ за один чек.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Інструкція НАЗК: Видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "Інша оплачувана робота. Поліцейським дозволено тільки: викладання, науку, творчість та медицину.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Інструкція НАЗК: Сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Якщо ви або сім'я входите до правління ГО, фондів чи кооперативів.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Інструкція НАЗК: Організації</a>")
}

# --- КЛАВІАТУРИ ТА ОБРОБНИКИ ---
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

@dp.message(Command("start"))
@dp.message(F.text == "⬅️ Назад")
async def start(message: types.Message):
    await message.answer("📋 <b>Головне меню</b>. Оберіть пункт:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Щорічна декларація за 2025 рік</b> подається до <b>31 березня 2026 року</b>.", parse_mode="HTML")

@dp.message(F.text == "👤 Адмін")
async def contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Альона</b>\n📞 <code>0660787241</code>", parse_mode="HTML")

@dp.message(F.text == "⚖️ Відповідальність")
async def resp(message: types.Message):
    await message.answer("⚖️ <b>Відповідальність:</b> Адмін (штрафи), Дисциплінарна (звільнення), Кримінальна.", parse_mode="HTML")

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
