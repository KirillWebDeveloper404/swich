from loader import dp, bot

from aiogram.types import Message
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(contains='О боте', ignore_case=True))
async def start(message: Message):
    await message.answer("""По любым вопросам можно обратиться в поддержку @swichsupportchat
Наш сайт - https://switch-moscow.ru""")
