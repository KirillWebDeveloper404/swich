import datetime
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, bot

from keyboards.default.main_menu import main_kb
from sql.User import User
from states.anketa import Anketa
from aiogram.dispatcher.storage import FSMContext


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        user = User.get(User.tg_id == message.from_user.id)
    except:
        user = User()
        user.tg_id = message.from_user.id
        user.name = 'register'
        user.status = 'Normal'
        user.save()

    await bot.send_photo(
        chat_id=message.from_user.id,
        photo=types.InputFile('img/start.png'),
        caption=f"Привет, {message.from_user.full_name}!\n" \
                f"Рады приветствовать тебя в SWITCH — создатель впечатлений, который всегда под рукой. \n"
                f"SWITCH всегда знает, что делать и поможет подборкой оригинальных занятий и любопытных мест в "
                f"Москве. \n"
                f"Для одного и для компании. \n"
                f"Давай наполним твою жизнь новыми событиями. Поехали! 🚀 \n",
        reply_markup=main_kb
    )

    if not (user.phone):
        await message.answer('Наш бот создан для знакомств, пожалуйста заполните информацию о себе')
        await Anketa.phone.set()
        await message.answer("Ваш номер телефона:",
                             reply_markup=ReplyKeyboardMarkup(
                                 [[KeyboardButton(text='Отправить номер телефона', request_contact=True)]],
                                 resize_keyboard=True
                             )
                             )


@dp.message_handler(content_types=['contact'], state=Anketa.phone)
async def phone(message: types.Message):
    print(message.contact)
    user = User.get(User.tg_id == message.from_user.id)
    user.phone = message.contact['phone_number']
    user.tarif = 'пробный период 7 дней'
    user.save()

    await Anketa.photo.set()
    await message.answer('Пришлите фото профиля:', reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=['photo'], state=Anketa.photo)
async def set_photo(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.photo = message.photo[-1].file_id
    user.save()

    await Anketa.name.set()
    await message.answer("Ваше имя:", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton(message.from_user.full_name)]
    ], resize_keyboard=True))


@dp.message_handler(state=Anketa.name)
async def name(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.name = message.text
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
    user.dead_line = datetime.datetime.today() + datetime.timedelta(days=7)
    user.save()

    await state.finish()

    await message.answer("Вы прошли регистрацию!", reply_markup=main_kb)
    # await message.answer(
    #    f"У вас действует бесплатная подписка на 7 дней. По её истечению вам будет необходимо перейти в раздел "
    #    f"Тарифы и оплатить один из предложенных.")


@dp.message_handler(Text(contains='Главное меню', ignore_case=True), state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Главное меню", reply_markup=main_kb)


@dp.callback_query_handler(text='main_menu', state='*')
async def main_menu_inline(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.answer("Главное меню", reply_markup=main_kb)
