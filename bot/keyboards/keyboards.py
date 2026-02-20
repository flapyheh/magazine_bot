from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.db.orm import select_all_products

async def create_catalog() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons : list[InlineKeyboardButton] = []
    
    products = await select_all_products()
    for product in products:
        button = InlineKeyboardButton(
            text=f'{product.title} - {product.price/100}{product.currency}',
            callback_data=f'product_{product.id}'
        )
        buttons.append(button)
    kb_builder.row(*buttons, width=1)
    
    return kb_builder.as_markup()