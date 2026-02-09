import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# --- КОНФІГУРАЦІЯ ---
TELEGRAM_TOKEN = "8532773844:AAF0I0Mpp6k_wPeoTXtoAlrlcaGXpTs8Qt4"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- ПОВНА БАЗА ЗНАНЬ З ПОСИЛАННЯМИ НА Wiki НАЗК ---
ANSWERS = {
    "Р1": ("📋 <b>Розділ 1: Вид декларації</b>\n\n"
           "Оберіть тип «Щорічна» та звітний період «2025 рік».\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/i-vydy-deklaratsij-ta-poryadok-yih-podannya/'>Інструкція: Види декларацій</a>"),

    "Р2": ("👤 <b>Розділ 2: Суб'єкт декларування</b>\n\n"
           "Перевірте ПІБ, РНОКПП, УНЗР та місце роботи. Вказуйте посаду, яку ви обіймали станом на 31.12.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/ii-vidomosti-pro-sub-yekta-deklaruvannya/'>Інструкція: Дані про суб'єкта</a>"),

    "Р2.1": ("👥 <b>Розділ 2.1: Члени сім'ї</b>\n\n"
             "Вказуються: чоловік/дружина, діти до 18 років та особи, що спільно проживали > 183 днів на рік.\n"
             "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/iii-chleny-sim-yi-sub-yekta-deklaruvannya/'>Інструкція: Члени сім'ї</a>"),

    "Р3": ("🏠 <b>Розділ 3: Об'єкти нерухомості</b>\n\n"
           "Власність, оренда та право користування (в т.ч. реєстрація місця проживання). Обов'язково вкажіть житло, де ви мешкали на 31.12.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/v-ob-yekty-neruhomosti/'>Інструкція: Нерухомість</a>"),

    "Р4": ("🏗️ <b>Розділ 4: Об'єкти незавершеного будівництва</b>\n\n"
           "Недобудоване майно, об'єкти не прийняті в експлуатацію або не зареєстровані в реєстрі.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vi-ob-yekty-nezavershenogo-budivnytstva/'>Інструкція: Будівництво</a>"),

    "Р5": ("💎 <b>Розділ 5: Цінне рухоме майно</b>\n\n"
           "Ювелірні вироби, техніка, антикваріат (якщо вартість > 100 ПМ, крім авто).\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/vii-ruhome-majno-krim-transportnyh-zasobiv/'>Інструкція: Цінне майно</a>"),

    "Р6": ("🚗 <b>Розділ 6: Транспортні засоби</b>\n\n"
           "Всі авто, мотоцикли, причепи, якими володіли або користувалися хоча б 1 день.\n"
           "🔗 <a href='https://wiki.nazk.gov.ua/category/deklaruvannya/viii-transportni-zasoby/'>Інструкція: Транспорт</a>"),

    "Р7": ("📈 <b>Розділ 7: Цінні папери</b>\n\n"
           "Акції, облігації, що належать вам або членам сім'ї.\n"
           "🔗 <a href='

