from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Bot token is missing! Set BOT_TOKEN in environment variables.")

print(f"Твой токен: {TOKEN}")
