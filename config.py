import os
from aiogram import Bot

TOKEN = os.getenv("BOT_TOKEN")  # Получаем токен из переменных окружения

if not TOKEN:
    raise ValueError("Bot token is missing! Set BOT_TOKEN in environment variables.")

bot = Bot(token=TOKEN)
