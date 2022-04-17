from loader import dp, bot
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text

import datetime

from sql import User, Who
from states import Ivent


@dp.message_handler(Text(contains='Найти мероприятие', ignore_case=True))
@dp.message_handler(text="Назад", state=Ivent.kategory)
async def start(message: types.Message):
    try:

        user = User.get(User.tg_id == message.from_user.id)

        groups = [el.name for el in Who.select()]
        keyboard = []

        for el in groups:
            keyboard.append([KeyboardButton(el)])

        keyboard.append([KeyboardButton('🔙Главное меню')])

        if datetime.datetime.strptime(user.dead_line.split('.')[0], "%Y-%m-%d %H:%M:%S") > datetime.datetime.today():

            await Ivent.started.set()

            await bot.send_photo(
                chat_id=message.from_user.id,
                photo=types.InputFile('img/selectcurs.png'),
                caption="Давай выберем, ты сегодня один или с компанией?",
                reply_markup=ReplyKeyboardMarkup(keyboard=keyboard,
                                                 resize_keyboard=True)
            )

        else:
            await message.answer("Упс... \n" \
                                 "У вас законфилась подписка \n\n" \
                                 "Перейдите в раздел тарифы и оплатите подписку")

    except Exception as e:
        pass
