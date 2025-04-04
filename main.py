import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.routers.basic import r as base_router

from settings.config import settings


async def bot_startup():
    bot = Bot(
        token=settings.TG_API,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    storage = None
    dp = Dispatcher()

    dp.include_routers(base_router)
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot start")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(bot_startup())
