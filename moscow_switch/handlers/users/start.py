import datetime
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
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
    user = User.get(User.tg_id == message.from_user.id)
    user.phone = message.contact['phone_number']
    user.tarif = 'пробный период 7 дней'
    user.dead_line = datetime.datetime.today() + datetime.timedelta(days=7)
    user.save()

    await Anketa.name.set()
    await message.answer("Ваше имя:", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton(message.from_user.full_name)]
    ], resize_keyboard=True))


@dp.message_handler(state=Anketa.name)
async def name(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.name = message.text
    user.save()

    await state.finish()

    await message.answer("Вы прошли регистрацию!", reply_markup=main_kb)
    await message.answer(
       f"У вас действует бесплатная подписка на 7 дней. По её истечению вам будет необходимо перейти в раздел "
       f"Тарифы и оплатить один из предложенных.")


@dp.message_handler(Text(contains='Главное меню', ignore_case=True), state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Главное меню", reply_markup=main_kb)


@dp.callback_query_handler(text='main_menu', state='*')
async def main_menu_inline(c: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await c.message.answer("Главное меню", reply_markup=main_kb)
