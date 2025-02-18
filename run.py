import asyncio
from aiogram import Bot, Dispatcher
from app.database.models import async_main
from app.handlers import router
from config import TOKEN
import app.database.requests as rq

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    await async_main()
    dp.include_router(router)
    asyncio.create_task(rq.passive_income_loop())
    print("✅ Bot is running!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
