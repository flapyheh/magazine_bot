import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery, PreCheckoutQuery, LabeledPrice, Message

from bot.db.orm import select_product, insert_order, change_status_order
from bot.config.config import settings
from bot.enums.enums import OrderStatuses
from bot.lexicon.lexicon import RU_USER

logger = logging.getLogger(__name__)
payments_router = Router()

@payments_router.callback_query()
async def process_product_button(call : CallbackQuery):
    result = call.data.split('_')
    product_id = result[1]
    
    product = await select_product(product_id)
    prices = [
        LabeledPrice(
            label=product.title,
            amount=product.price
        )
    ]
    
    await insert_order(
        user_id=call.message.from_user.id,
        product_id=product_id,
        payment_id=None,
        status=OrderStatuses.pending
    )
    
    await call.message.answer_invoice(
        title=product.title,
        description=product.description,
        payload=f"product_{product.id}",
        provider_token=settings.bot.PAYMENTS_PROVIDER_TOKEN,
        currency=product.currency,
        prices=prices
    )
    await call.message.delete(call.message.message_id)
    
@payments_router.pre_checkout_query()
async def pre_checkout(precheckout : PreCheckoutQuery):
    await precheckout.answer(ok=True)
    
@payments_router.message(lambda message: message.successful_payment)
async def process_successful_payment(message : Message):
    payment = message.successful_payment
    product_id = int(payment.invoice_payload.split('_')[1])
    
    await change_status_order(status=OrderStatuses.paid, payment_id=payment.telegram_payment_charge_id)
    await message.answer(RU_USER['payment_success'])
    
    product = await select_product(product_id)
    await message.answer_document(document=product.file_path)