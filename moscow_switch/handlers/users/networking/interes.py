from loader import dp, bot

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from sql import User
from keyboards.default import main_kb


@dp.callback_query_handler(text='like', state='*')
async def like(c: CallbackQuery, state: FSMContext):
    try:
        user_to = User.get(User.tg_id == c.message.text.split('\n')[0].replace('#', ''))
        user = User.get(User.tg_id == c.from_user.id)
    except:
        user_to = User.get(User.tg_id == c.message.caption.split('\n')[0].replace('#', ''))
        user = User.get(User.tg_id == c.from_user.id)

    info = f'#{user.tg_id}\n'
    info += f"Имя: {user.name} \n"
    info += f"Возраст: {user.age} \n"
    info += f"Вид деятельности: {user.profession} \n"
    info += f"Интересы: {user.field_activity} \n"
    info += f"Рост: {user.length} \n"
    info += f"Вес: {user.weight} \n"

    await bot.send_message(chat_id=user_to.tg_id,
                           text='С вами хотят познакомиться. Отправить пользователю ваш контакт?')
    try:
        await bot.send_photo(chat_id=user_to.tg_id, photo=user.photo, caption=info,
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                 InlineKeyboardButton(text='Отправить свой контакт', callback_data='send_contact')))
        await c.message.answer('Отправили заявку на знакомство, если этот пользователь захочет поделиться контактом '
                               'мы вам напишем.')
    except Exception as e:
        await bot.send_message(chat_id=user_to.tg_id, text=info, reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='Отправить свой контакт', callback_data='send_contact')))
        await c.message.answer('Отправили заявку на знакомство, если этот пользователь захочет поделиться контактом '
                               'мы вам напишем.')


@dp.callback_query_handler(text='send_contact', state='*')
async def send_contact(c: CallbackQuery, state: FSMContext):
    await state.finish()
    try:
        user_to = User.get(User.tg_id == c.message.text.split('\n')[0].replace('#', ''))
        user = User.get(User.tg_id == c.from_user.id)
    except:
        user_to = User.get(User.tg_id == c.message.caption.split('\n')[0].replace('#', ''))
        user = User.get(User.tg_id == c.from_user.id)

    info = f'Пользователь одобрил вашу заявку на знакомство. Вы можете с ним связаться по телефону \n\n'
    info += f"Имя: {user.name} \n"
    info += f"Номер телефона: {user.phone} \n"
    info += f"Возраст: {user.age} \n"
    info += f"Интересы: {user.field_activity} \n"
    info += f"Рост: {user.length} \n"
    info += f"Вес: {user.weight} \n"

    info1 = f'Вы одобрил заявку на знакомство. Вы можете с ним связаться по телефону \n\n'
    info1 += f"Имя: {user.name} \n"
    info1 += f"Номер телефона: {user.phone} \n"
    info1 += f"Возраст: {user.age} \n"
    info1 += f"Интересы: {user.field_activity} \n"
    info1 += f"Рост: {user.length} \n"
    info1 += f"Вес: {user.weight} \n"

    try:
        await bot.send_photo(chat_id=user_to.tg_id, photo=user.photo, caption=info, reply_markup=ReplyKeyboardMarkup(
            [
                [KeyboardButton('Главное меню')]
            ],
            resize_keyboard=True
        ))
        await bot.send_photo(chat_id=user.tg_id, photo=user_to.photo, caption=info1, reply_markup=main_kb)
        await state.finish()
    except Exception as e:
        await bot.send_message(chat_id=user_to.tg_id, text=info, reply_markup=main_kb)
        await bot.send_message(chat_id=user.tg_id, text=info1, reply_markup=main_kb)
        await state.finish()

