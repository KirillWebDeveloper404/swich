from loader import dp, Bot

import datetime
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.inline import search_kb
from states import Networking, Anketa
from sql import User


@dp.message_handler(Text(contains='нетворкинг', ignore_case=True))
async def start(message: Message, state: FSMContext):
    try:
        user = User.get(User.tg_id == message.from_user.id)

        if user.age == None:
            await message.answer("Похоже вы у нас в первый раз, заполните анкету о себе чтобы начать общаться с другими.")
            await message.answer("Пришлите ваше фото")
            await Anketa.photo.set()
            return 0

        if datetime.datetime.strptime(user.dead_line.split('.')[0], "%Y-%m-%d %H:%M:%S") > datetime.datetime.today():
            data = {
                'age_min': 0,
                'len_min': 0,
                'age_max': 10000,
                'len_max': 10000,
                'weight_min': 0,
                'weight_max': 10000
            }

            # Clear keyboard
            _ck_ = await message.answer('<code>Clearing keyboard...</code>', reply_markup=types.ReplyKeyboardRemove())
            await _ck_.delete()

            await message.answer("Здась ты можешь найти и познакомиться с другими людьми. \nДля поиска выберите "
                                 "фильтры и "
                                 "нажмите найти",
                                 reply_markup=search_kb)
            await Networking.started.set()
            await state.update_data(data)

        else:
            await message.answer(
                "Упс... \n""У вас законфилась подписка \n\nПерейдите в раздел тарифы и оплатите подписку")

    except Exception as e:
        print(e)
        await message.answer("Упс... \n""У вас законфилась подписка \n\nПерейдите в раздел тарифы и оплатите подписку")


@dp.message_handler(content_types=['photo'], state=Anketa.photo)
async def set_photo(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.photo = message.photo[-1].file_id
    user.save()

    await Anketa.profi.set()
    await message.answer("Напиши о своей профессии, кем ты работаешь?", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.profi)
async def set_interes(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.profession = message.text
    user.save()

    await Anketa.field_activity.set()
    await message.answer("Напиши о своих интересах, чем ты увлекаешься?", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.field_activity)
async def activity(message: types.Message):
    text = message.text
    if len(text) > 10:

        user = User.get(User.tg_id == message.from_user.id)
        user.field_activity = text
        user.save()

        await Anketa.lenght.set()
        await message.answer("Какого вы роста(в см):")

    else:

        await Anketa.field_activity.set()
        await message.answer("Слишком коротко, напишите более подробно:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.lenght)
async def leng(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.length = message.text
    user.save()

    await Anketa.weight.set()
    await message.answer("Ваш вес:")


@dp.message_handler(state=Anketa.weight)
async def weight(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.weight = message.text
    user.save()

    await Anketa.age.set()
    await message.answer("Сколько вам лет:")


@dp.message_handler(state=Anketa.age)
async def age(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.age = message.text
    user.save()

    data = {
                'age_min': 0,
                'len_min': 0,
                'age_max': 10000,
                'len_max': 10000,
                'weight_min': 0,
                'weight_max': 10000
            }

    await message.answer("Здась ты можешь найти и познакомиться с другими людьми. \nДля поиска выберите "
                                 "фильтры и "
                                 "нажмите найти",
                                 reply_markup=search_kb)
    await Networking.started.set()
    await state.update_data(data)
