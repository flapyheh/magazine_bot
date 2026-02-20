from aiogram.filters import BaseFilter
from aiogram.types import Message

from bot.config.config import settings

class IsAdmin(BaseFilter):
    async def __call__(self, message : Message) -> bool:
        if message.from_user.id in settings.bot.ADMIN_IDS:
            return True
        else:
            return False