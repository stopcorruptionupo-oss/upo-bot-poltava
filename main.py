import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ (УСІ 18 РОЗДІЛІВ РОЗГОРНУТО) ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Оберіть тип «Щорічна» та звітний період «2025 рік». "
           "Якщо ви подаєте декларацію вперше після призначення — «Кандидата на посаду». "
           "Якщо звільняєтесь — «При звільненні».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Докладніше про види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "🏢 Місце роботи: <b>Управління поліції охорони в Полтавській області</b>.\n"
           "🏷 Код ЄДРПОУ: <b>40109042</b>.\n"
           "⚠️ <b>ВАЖЛИВО:</b> У полі 'Категорія посади' обов'язково обирайте — <b>НЕ ЗАСТОСОВУЄТЬСЯ</b>. "
           "Також вкажіть ваш УНЗР (13 цифр з ID-картки).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Докладніше про дані суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Вписуємо подружжя (навіть якщо проживаєте окремо, але шлюб не розірвано), дітей до 18 років та осіб, що спільно проживали понад 183 дні протягом року.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Докладніше про членів сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Нерухомість</b>\n\n"
           "Вказуємо власність, оренду чи право користування (прописку) суб'єкта ТА сім'ї. "
           "Обов'язково вкажіть житло, де ви фактично проживали станом на 31.12.2025.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Докладніше про нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Незавершене будівництво</b>\n\n"
           "Декларуємо об'єкти, які ще не прийняті в експлуатацію або право власності на які не зареєстровано в реєстрі. "
           "Це стосується як ваших об'єктів, так і майна сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Докладніше про недобудови</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Дорогі речі (ювелірка, антикваріат), вартість яких перевищує 100 прожиткових мінімумів. Автомобілі сюди НЕ вносяться.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Докладніше про цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Вказуємо всі авто суб'єкта ТА сім'ї: власність, користування за техпаспортом чи довіреністю. "
           "Навіть якщо ви користувалися машиною хоча б один день.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Докладніше про транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації (включаючи військові ОВДП), сертифікати, що належать вам або членам вашої сім'ї.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ih-tsinni-papery/'>Докладніше про цінні папери</a>"),

    "Р8": ("🏢 <b>Розділ 8: Корпоративні права</b>\n\n"
           "⚠️ <b>ПОЛІЦЕЙСЬКИМ ЗАБОРОНЕНО</b> мати частки в прибуткових фірмах. "
           "Якщо ви маєте частку в ТОВ, вона повинна бути передана в управління (траст).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/h-korporatyvni-prava/'>Докладніше про корп. права</a>"),

    "Р9": ("🏢 <b>Розділ 9: Бенефіціарна власність</b>\n\n"
           "Декларуємо юридичні особи, контроль над якими ви або сім'я здійснюєте через третіх осіб або офшори.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hi-yurydychni-osoby-trasty-abo-inshi-podibni-pravovi-utvorennya-kintsevym-benefitsiarnym-vlasnykom-kontrolerom-yakyh-ye-sub-yekt-deklaruvannya-abo-chleny-jogo-sim-yi/'>Докладніше про бенефіціарів</a>"),

    "Р10": ("💡 <b>Розділ 10: Нематеріальні активи</b>\n\n"
            "🟡 <b>Криптовалюти:</b> вказуємо назву (BTC, ETH), кількість монет, дату набуття та ідентифікатор гаманця. Також сюди пишуться патенти та авторські права.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hii-nematerialni-aktyvy/'>Докладніше про активи</a>"),

    "Р11": ("💰 <b>Розділ 11: Доходи та подарунки</b>\n\n"
            "Зарплата (повна сума до вирахування податків), пенсія, соцвиплати, допомога ВПО, аліменти, відсотки — ваші та СІМ'Ї.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiii-dohody-u-tomu-chysli-podarunky/'>Докладніше про доходи</a>"),

    "Р12": ("💵 <b>Розділ 12: Грошові активи</b>\n\n"
            "Готівка, гроші на банківських картках, внески у кредитні спілки. Декларується, якщо загальна сума (ваша + сім'ї) перевищує 50 ПМ.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/hiv-groshovi-aktyvy/'>Докладніше про гроші</a>"),

    "Р12.1": ("💳 <b>Розділ 12.1: Банківські установи</b>\n\n"
              "⚠️ <b>ТІЛЬКИ НАЗВИ БАНКІВ.</b> Обираємо зі списку банки, де відкрито рахунки у вас або сім'ї. Номери рахунків (IBAN) вписувати НЕ потрібно.\n"
              "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xv-bankivski-ta-inshi-finansovi-ustanovy/'>Докладніше про рахунки</a>"),

    "Р13": ("📉 <b>Розділ 13: Фінансові зобов’язання</b>\n\n"
            "Кредити, отримані позики, залишки боргу по кредитних лімітах карт (якщо борг станом на 31.12 перевищує 50 ПМ).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvi-finansovi-zobov-yazannya/'>Докладніше про зобов'язання</a>"),

    "Р14": ("🧾 <b>Розділ 14: Видатки та правочини</b>\n\n"
            "Разові витрати СУБ'ЄКТА (поліцейського) понад 50 ПМ (покупка майна, оплата послуг тощо).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xvii-vydatky-ta-pravochyny/'>Докладніше про видатки</a>"),

    "Р15": ("⚠️ <b>Розділ 15: Робота за сумісництвом</b>\n\n"
            "Поліцейським заборонено іншу оплачувану діяльність, крім викладацької, наукової, творчої чи медичної.\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xviii-robota-za-sumisnytstvom/'>Докладніше про сумісництво</a>"),

    "Р16": ("🏛️ <b>Розділ 16: Членство в організаціях</b>\n\n"
            "Участь у керівних чи наглядових органах ГО, благодійних фондів, профспілок (ваші або членів сім'ї).\n"
            "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/xix-vhodzhennya-do-kerivnyh-revizijnyh-chy-naglyadovyh-organiv/'>Докладніше про членство</a>")
}

# --- КЛАВІАТУРИ ---

def main_menu():
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="📥 Автозаповнення декларації"))
    builder.row(types.KeyboardButton(text="🔍 Автоперевірка своєї декларації"))
    builder.row(types.KeyboardButton(text="📂 Розділи декларування"))
    builder.row(types.KeyboardButton(text="📅 Терміни подання"))
    builder.row(types.KeyboardButton(text="👤 Адміністратор"), types.KeyboardButton(text="⚖️ Відповідальність"))
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
    await message.answer("📋 <b>Головне меню Полтавського УПО</b>. Оберіть потрібний розділ:", reply_markup=main_menu(), parse_mode="HTML")

@dp.message(F.text == "📥 Автозаповнення декларації")
async def auto_fill(message: types.Message):
    await message.answer(
        "📥 <b>Автозаповнення декларації</b>\n\nСкористайтеся інструкцією за посиланням:\n"
        "🔗 <a href='https://drive.google.com/file/d/1sYUYtHR34JD07oPRl-lFI_cWeKRXZyoO/view?usp=sharing'>Переглянути інструкцію</a>",
        parse_mode="HTML"
    )

@dp.message(F.text == "🔍 Автоперевірка своєї декларації")
async def auto_check(message: types.Message):
    text = (
        "<b>🔍 Автоперевірка своєї декларації</b>\n\n"
        "Шановний користувач! \n\nСкористайся «Автоперевіркою своєї декларації».\n\n"
        "1️⃣ Зайди за посиланням та авторизуйся: https://www.integrity-police.pp.ua/Perevirka-deklaratsiyi\n"
        "«Ваш підрозділ/орган – обирай <b>ДЕПАРТАМЕНТ ПОЛІЦІЇ ОХОРОНИ</b>»\n\n"
        "2️⃣ За посиланням https://public.nazk.gov.ua/ в пошуку заповни свої ПІБ, після чого скопіюй посилання на власну Декларацію.\n\n"
        "3️⃣ Встав його у поле перевірки попереднього ресурсу, далі натисни «Згенеруй Декларацію», після чого натисни на «Звіт по декларації».\n\n"
        "⚠️ В результаті буде сформований звіт Правильності поданої декларації з можливими помилками, які будуть виділені <b>червоним кольором</b>."
    )
    await message.answer(text, parse_mode="HTML", disable_web_page_preview=True)

@dp.message(F.text == "⚖️ Відповідальність")
async def responsibility(message: types.Message):
    text = (
        "⚖️ <b>Відповідальність за завідомо недостовірні відомості в декларації:</b>\n\n"
        "🟥 <b>Кримінальна:</b> понад 750 ПМ* (понад 2 271 000 грн у 2025 році; понад 2 496 000 грн у 2026 році).\n\n"
        "🟧 <b>Адміністративна:</b> від 150 до 750 ПМ* (від 454 200 грн до 2 271 000 грн у 2025 році; від 499 200 грн до 2 496 000 грн у 2026 році).\n\n"
        "🟨 <b>Дисциплінарна</b> (догана, сувора догана, звільнення тощо): до 150 ПМ* (до 454 200 грн у 2025 році; до 499 200 грн у 2026 році).\n\n"
        "<i>* 1 ПМ у 2025 році = 3028 грн</i>\n"
        "<i>  1 ПМ у 2026 році = 3328 грн</i>"
    )
    await message.answer(text, parse_mode="HTML")

@dp.message(F.text == "👤 Адміністратор")
async def admin_contact(message: types.Message):
    await message.answer("👤 <b>Адміністратор Альона</b>\n📞 <code>0660787241</code>", parse_mode="HTML")

@dp.message(F.text == "📅 Терміни подання")
async def terms(message: types.Message):
    await message.answer("📅 <b>Терміни подання:</b>\n\nЩорічна декларація за 2025 рік подається з 1 січня до <b>31 березня 2026 року</b> включно.", parse_mode="HTML")

@dp.message(F.text == "📂 Розділи декларування")
async def show_sections(message: types.Message):
    await message.answer("📝 Оберіть номер розділу для отримання довідки:", reply_markup=sections_menu(), parse_mode="HTML")

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
