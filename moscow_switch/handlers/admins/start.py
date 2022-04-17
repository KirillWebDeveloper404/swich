from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from loader import dp, bot
from sql import Admin, User


class Ads(StatesGroup):
    photo = State()
    text = State()
    send = State()


@dp.message_handler(text='/admin', state='*')
@dp.message_handler(text='Назад к админке', state='*')
@dp.message_handler(text='Отмена', state='*')
async def bot_start_admin(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        admin = Admin.get(Admin.tg_id == message.from_user.id)

        await message.answer(
            f"Привет админ {message.from_user.full_name}",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Создать рассылку')],
                    [KeyboardButton('Главное меню(пользователь)')]
                ],
                resize_keyboard=True
            )
        )

    except:
        pass


@dp.message_handler(Text(contains='создать рассылку', ignore_case=True))
async def ads(message: types.Message, state: FSMContext):
    try:
        admin = Admin.get(Admin.tg_id == message.from_user.id)

        await message.answer(
            f"Пришли фото для рассылки",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Без фото')],
                    [KeyboardButton('Назад к админке')]
                ],
                resize_keyboard=True
            )
        )

        await Ads.photo.set()

    except:
        pass


@dp.message_handler(content_types=['photo'], state=Ads.photo)
@dp.message_handler(Text(contains='без фото', ignore_case=True))
async def ads(message: types.Message, state: FSMContext):
    try:
        admin = Admin.get(Admin.tg_id == message.from_user.id)
        await Ads.text.set()
        if len(message.photo):
            await state.update_data({'photo': message.photo[-1].file_id})

        await message.answer(
            f"Пришли текст рассылки",
            reply_markup=ReplyKeyboardRemove()
        )

    except:
        pass


@dp.message_handler(state=Ads.text)
async def text(message: types.Message, state: FSMContext):
    try:
        admin = Admin.get(Admin.tg_id == message.from_user.id)
        await state.update_data({'text': message.text})
        data = await state.get_data()

        try:
            await bot.send_photo(
                message.from_user.id,
                data['photo'],
                caption=data['text']
            )
        except Exception as e:
            await message.answer(data['text'])

        await message.answer(
            f"Запустить рассылку?",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Запустить рассылку')],
                    [KeyboardButton('Отмена')]
                ],
                resize_keyboard=True
            )
        )
        await Ads.send.set()
    except:
        pass


@dp.message_handler(text='Запустить рассылку', state=Ads.send)
async def bot_start_admin(message: types.Message, state: FSMContext):
    try:
        admin = Admin.get(Admin.tg_id == message.from_user.id)
        users = [el.tg_id for el in User.select()]
        data = await state.get_data()

        adresats = 0
        block = 0

        for user in users:
            try:
                try:
                    await bot.send_photo(user, data['photo'], caption=data['text'])
                except:
                    await bot.send_message(user, data['text'])
                adresats += 1
            except:
                block += 1

        await message.answer(f"Рассылка успешна доставлена пользователям {adresats}\nНе получило рассылку {block}, потому что заблокировали бота")
        await message.answer(
            f"Главное меню администратора",
            reply_markup=ReplyKeyboardMarkup(
                [
                    [KeyboardButton('Создать рассылку')],
                    [KeyboardButton('Главное меню(пользователь)')]
                ],
                resize_keyboard=True
            )
        )

    except:
        pass
