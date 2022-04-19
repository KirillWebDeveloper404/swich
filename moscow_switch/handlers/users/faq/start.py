from loader import dp, bot

from aiogram.types import Message
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(contains='faq', ignore_case=True))
async def start(message: Message):
    await message.answer('В разработке...')