import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from bot.core.logger import configure_logging
from bot.middlewares.throttling import AntiSpamMiddleware
from redis.asyncio import Redis

from bot.core.config import settings
from bot.handlers.common import router as common_router
from bot.middlewares.database import DatabaseMiddleware
from bot.middlewares.i18n import I18nMiddleware
from bot.tasks.broker import broker

logger = logging.getLogger(__name__)


async def main():
    configure_logging()
    logger.info("Starting bot deployment...")

    bot = Bot(
        token=settings.TELEGRAM_BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    redis_client = Redis.from_url(settings.redis_url)
    storage = RedisStorage(redis=redis_client)

    dp = Dispatcher(storage=storage)

    # Global middlewares
    dp.update.outer_middleware(DatabaseMiddleware())
    dp.update.outer_middleware(I18nMiddleware())
    dp.message.middleware(AntiSpamMiddleware())

    # Routers
    dp.include_router(common_router)

    # Start Taskiq broker
    await broker.startup()

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await broker.shutdown()
        await bot.session.close()
        await redis_client.aclose()
        logger.info("Bot stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Session terminated by user.")
