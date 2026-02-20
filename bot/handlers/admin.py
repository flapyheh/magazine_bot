import logging
import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from bot.db.orm import add_product

logger = logging.getLogger(__name__)
admin_router = Router()

@admin_router.message(Command('add_product'))
async def process_adding_product(message : Message, admin_ids : list[int]) -> None:
    if message.from_user.id not in admin_ids:
        return
    args = message.text.split(' ')
    if len(args) != 6:
        message.answer('Введите новый товар правильно: /add_product <title> <description> <price (в копейках)> <file path>')
        return
    if os.path.exists(args[4]):
        await add_product(title=args[1], description=args[2], price=args[3], filepath=args[4])
        logger.info(f'Продукт {args[1]} добавлен')
        await message.answer(f'Продукт {args[1]} добавлен')
    else:
        await message.answer('Неправильно введен путь до файла')
        logger.warning('Неправильно ввели путь до файла!')