import asyncio
import logging

from bot.bot import main
from bot.config.config import settings

logging.basicConfig(
    level=logging.getLevelName(level=settings.log.log_level),
    format=settings.log.log_format,
)

asyncio.run(main())