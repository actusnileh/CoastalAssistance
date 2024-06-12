import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from database.database import create_tables
from misc.maps import start_map

from config import settings as settings_config

from handlers import registration
from handlers import settings
from handlers import add_pic
from handlers import admin_panel
from handlers import about_photo
from handlers import list_added
from handlers import help


async def main():
    await create_tables()
    await start_map()

    bot = Bot(token=settings_config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(registration.router)

    dp.include_router(settings.router)
    dp.include_router(add_pic.router)
    dp.include_router(help.router)
    dp.include_router(admin_panel.router)
    dp.include_router(list_added.router)
    dp.include_router(about_photo.router)
    await bot.delete_webhook(drop_pending_updates=True)

    print("Бот успешно запущен.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
