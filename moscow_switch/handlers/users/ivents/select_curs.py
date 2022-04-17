from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

import datetime

from sql import User, Who, Kategory
from states import Ivent


@dp.message_handler(state=Ivent.started)
async def curs_list(message: types.Message, state: FSMContext):
    who = Who.get(Who.name == message.text)

    await Ivent.kategory.set()
    await state.update_data({'group': message.text})

    kategorys = [el.name for el in Kategory.select().where(Kategory.for_who == who.id)]
    await state.update_data({'who_id': who.id})
    keyboard = []

    for el in kategorys:
        keyboard.append([KeyboardButton(el)])

    keyboard.append([KeyboardButton('Назад')])

    await message.answer(text='Выберем направление',
                         reply_markup=ReplyKeyboardMarkup(keyboard,
                                                          resize_keyboard=True)
                         )


@dp.message_handler(state=Ivent.places_group, text='Назад')
async def curs_list(message: types.Message, state: FSMContext):
    data = await state.get_data()
    who = Who.get(Who.id == data['who_id'])

    await Ivent.kategory.set()
    await state.update_data({'group': message.text})

    kategorys = [el.name for el in Kategory.select().where(Kategory.for_who == who.id)]
    await state.update_data({'who_id': who.id})
    keyboard = []

    for el in kategorys:
        keyboard.append([KeyboardButton(el)])

    keyboard.append([KeyboardButton('Назад')])

    await message.answer(text='Выберем направление',
                         reply_markup=ReplyKeyboardMarkup(keyboard,
                                                          resize_keyboard=True)
                         )
