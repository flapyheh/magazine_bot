import logging

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from bot.lexicon.lexicon import RU_USER
from bot.db.orm import add_user
from bot.keyboards.keyboards import create_catalog

logger = logging.getLogger(__name__)
user_router = Router()

@user_router.message(CommandStart())
async def process_user_command_start(message : Message):
    await message.answer(RU_USER['start'])
    await add_user(id=message.from_user.id, username=message.from_user.username)

@user_router.message(Command('help'))
async def process_user_help_command(message : Message):
    await message.answer(RU_USER['help'])

@user_router.message(Command('catalog'))
async def process_user_catalog_command(message : Message):
    keyboard = await create_catalog()
    await message.answer(
        text=RU_USER['catalog'],
        reply_markup=keyboard
    )