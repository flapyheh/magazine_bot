import logging
import os
import shlex

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

from bot.db.orm import add_product
from bot.filters.AdminFilter import IsAdmin
from bot.fsm.States import AddProductFSM

logger = logging.getLogger(__name__)
admin_router = Router()

@admin_router.message(Command('add_product'))
async def process_adding_product(message : Message, state : FSMContext) -> None:
    await state.set_state(AddProductFSM.name)
    await message.answer('Введите название товара:')
        
@admin_router.message(AddProductFSM.name)
async def process_adding_name(message : Message, state : FSMContext):
    await state.update_data(name=message.text)
    
    await state.set_state(AddProductFSM.description)
    await message.answer('Введите описание товара:')

@admin_router.message(AddProductFSM.description)
async def process_adding_desc(message : Message, state : FSMContext):
    await state.update_data(description=message.text)
    
    await state.set_state(AddProductFSM.price)
    await message.answer('Введите цену товара (В КОПЕЙКАХ!):')

@admin_router.message(AddProductFSM.price)
async def process_adding_desc(message : Message, state : FSMContext):
    if not message.text.isdigit() or int(message.text) < 100:
        await message.answer('Цена должна быть числом и больше 1 рубля!')
        return
    
    await state.update_data(price=int(message.text))
    await state.set_state(AddProductFSM.filepath)
    await message.answer('Введите путь до товара (пример: files/name.txt):')
    
@admin_router.message(AddProductFSM.filepath)
async def process_adding_desc(message : Message, state : FSMContext):
    if not os.path.exists(message.text):
        await message.answer('Путь не найден, введите его корректно еще раз')
        logger.warning('Неправильно ввели путь до файла!')
        return
    
    await state.update_data(filepath=message.text)
    data = await state.get_data()
    await state.clear()

    await add_product(title=data["name"], description=data["description"], price=data["price"], filepath=data["filepath"])
    logger.info(f'Продукт {data["name"]} добавлен')
    await message.answer(f'Продукт {data["name"]} добавлен')