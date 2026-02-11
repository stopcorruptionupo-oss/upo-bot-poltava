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
           "Обираємо тип «Щорічна». Звітний період — 2025 рік. "
           "Якщо ви подаєте вперше після призначення — «Кандидата на посаду». "
           "Якщо звільняєтесь — «При звільненні».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Wiki НАЗК: Види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "ПІБ, РНОКПП, УНЗР (13 цифр з ID-картки).\n"
           "🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>. Код ЄДРПОУ: <b>40109042</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Wiki НАЗК: Суб'єкт декларування</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Вписуємо подружжя (навіть якщо проживаєте окремо, але в шлюбі), дітей до 18 років та осіб, що спільно проживають понад 183 дні.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Wiki НАЗК: Члени сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n"
           "Власність, оренда та право проживання (прописка) вас та сім'ї. Обов'язково вкажіть об'єкт, де ви та сім'я жили на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Wiki НАЗК: Нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Об'єкти, що будуються, або не прийняті в експлуатацію. Сюди також відносимо майно членів сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Wiki НАЗК: Будівництво</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Ювелірні вироби, техніка, антикваріат дорожче 100 ПМ (понад 302 800 грн). Авто сюди не пишемо!\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Wiki НАЗК: Цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Ваші авто та авто сім'ї. Вказуємо все: власність, користування по техпаспорту чи довіреності.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Wiki НАЗК: Транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації (включаючи військові), що належать вам або членам вашої сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Wiki НАЗК: Цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "⚠️ <b>ДЛЯ ПОЛІЦЕЙСЬКИХ:</b> Заборонено входити до правління прибуткових фірм. "
           "Якщо ви маєте частку в ТОВ, вона мала бути передана в управління. Члени сім'ї вказують свої частки без обмежень.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Wiki НАЗК: Корпоративні права</a>"),

    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Фірми, якими ви або сім'я володієте не напряму, а через посередників.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Wiki НАЗК: Бенефіціари</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "🟡 <b>Криптовалюти:</b> Назва (BTC, ETH), кількість, дата набуття, біржа/гаманець.\n"
            "🟡 <b>Авторські права:</b> Патенти, літературні праці, знаки для товарів.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Wiki НАЗК: Нематеріальні активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "Ваші та ВСІХ членів сім'ї. Зарплата (брутто), пенсія, допомога ВПО, аліменти, відсотки, подарунки.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Wiki НАЗК: Доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка та гроші на рахунках. Декларується, якщо загальна сума (ви + сім'я) перевищує 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Wiki НАЗК: Грошові активи</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські рахунки</b>\n\n"
              "<b>⚠️ ТІЛЬКИ НАЗВИ БАНКІВ:</b>\n"
              "Обираємо зі списку назви банків (Приват, Ощад, Монобанк тощо), де у вас або сім'ї відкриті рахунки (навіть якщо там 0 грн).\n"
              "• Номери IBAN вписувати НЕ потрібно.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Wiki НАЗК: Рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, позики, ліміти по картках (ваші та сім'ї), якщо залишок боргу на 31.12 > 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Wiki НАЗК: Зобов'язання</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Тільки ВАШІ особисті витрати (як суб'єкта) понад 50 ПМ за один чек за звітний рік.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Wiki НАЗК: Видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "Інша робота. Поліцейським дозволено тільки: викладання, науку, творчість та медицину.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Wiki НАЗК: Сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Участь у керівних чи наглядових органах ГО, фондів, кооперативів ваші або сім'ї.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Wiki НАЗК: Членство</a>")
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
    # Створюємо кнопки для всіх 18 розділів
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
    await message.answer("⚖️ <b>Відповідальність:</b>\n• Адміністративна (штраф)\n• Дисциплінарна (звільнення)\n• Кримінальна (за недостовірні відомості).", parse_mode="HTML")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
