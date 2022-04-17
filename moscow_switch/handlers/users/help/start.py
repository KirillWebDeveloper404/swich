from loader import dp, bot

from aiogram.types import Message
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(contains='О боте', ignore_case=True))
async def start(message: Message):
    await message.answer("""По любым вопросам можно обратиться в поддержку @swichsupportchat
Наш сайт - https://switch-moscow.ru

Владелец - ООО "СВИЧ", ОГРН 0000000000000, ИНН 0000000000

Пользуясь мной, ты принимаешь условия Пользовательского соглашения""")
