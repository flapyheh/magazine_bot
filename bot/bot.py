import logging

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers.admin import admin_router
from bot.handlers.user import user_router
from bot.handlers.payments import payments_router
from bot.config.config import settings
from bot.db.orm import create_tables
from bot.filters.AdminFilter import IsAdmin

logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main() -> None:
    logger.info("Creating bot...")
    bot = Bot(token=settings.bot.BOT_TOKEN)
    
    # Инициализируем dispatcher
    logger.info("Initialize dp...")
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    logger.info('Creating DB tables...')
    await create_tables()
    
    # Подключаем роутеры в нужном порядке
    logger.info("Including routers...")
    dp.include_routers(admin_router, payments_router, user_router)
    admin_router.message.filter(IsAdmin())

    # Запускаем поллинг
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(e)