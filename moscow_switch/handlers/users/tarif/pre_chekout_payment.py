from aiogram import types
from loader import bot, dp

from states.tarifs import Tarif


@dp.pre_checkout_query_handler(state=Tarif.select)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)