from loader import dp, bot

from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from states import Profile
from sql import User


@dp.message_handler(Text(contains='профиль', ignore_case=True))
async def start(message: Message):

    await Profile.started.set()

    user = User.get(User.tg_id == message.from_user.id)

    info = "Ваши данные: \n"
    info+=f"Имя: {user.name} \n"
    info+=f"Возраст: {user.age} \n"
    info += f"Вид деятельности: {user.profession} \n"
    info+=f"Интересы: {user.field_activity} \n"
    info+=f"Рост: {user.length} \n"
    info+=f"Вес: {user.weight} \n"

    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='📷 Фото профиля', callback_data='edit_photo'),
        InlineKeyboardButton(text='🙋 Имя', callback_data='edit_name')).add(
        InlineKeyboardButton(text='🔢 Возраст', callback_data='edit_age')).add(
        InlineKeyboardButton(text='🧰 Интересы', callback_data='edit_act'),).add(
        InlineKeyboardButton(text='🛠 Вид деятельности', callback_data='edit_profi')).add(
        InlineKeyboardButton(text='📏 Рост', callback_data='edit_len'),
        InlineKeyboardButton(text='⚖️ Вес', callback_data='edit_weight')).add(
        InlineKeyboardButton(text='🔙 Главное меню', callback_data='main_menu'))

    # Clear keyboard
    _ck_ = await message.answer('<code>Clearing keyboard...</code>', reply_markup=ReplyKeyboardRemove())
    await _ck_.delete()

    if user.photo:
        await bot.send_photo(message.from_user.id, user.photo, caption=info, reply_markup=keyboard)
    else:
        await message.answer(info, reply_markup=keyboard)


async def start_c(c: CallbackQuery):

    await Profile.started.set()

    user = User.get(User.tg_id == c.from_user.id)

    info = "Ваши данные: \n"
    info+=f"Имя: {user.name} \n"
    info+=f"Возраст: {user.age} \n"
    info += f"Вид деятельности: {user.profession} \n"
    info+=f"Интересы: {user.field_activity} \n"
    info+=f"Рост: {user.length} \n"
    info+=f"Вес: {user.weight} \n"

    keyboard = InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton(text='📷 Фото профиля', callback_data='edit_photo'),
        InlineKeyboardButton(text='🙋 Имя', callback_data='edit_name')).add(
        InlineKeyboardButton(text='🔢 Возраст', callback_data='edit_age')).add(
        InlineKeyboardButton(text='🧰 Интересы', callback_data='edit_act'),).add(
        InlineKeyboardButton(text='🛠 Вид деятельности', callback_data='edit_profi')).add(
        InlineKeyboardButton(text='📏 Рост', callback_data='edit_len'),
        InlineKeyboardButton(text='⚖️ Вес', callback_data='edit_weight')).add(
        InlineKeyboardButton(text='🔙 Главное меню', callback_data='main_menu'))

    # Clear keyboard
    _ck_ = await c.message.answer('<code>Clearing keyboard...</code>', reply_markup=ReplyKeyboardRemove())
    await _ck_.delete()

    if user.photo:
        await bot.send_photo(c.from_user.id, user.photo, caption=info, reply_markup=keyboard)
    else:
        await c.message.answer(info, reply_markup=keyboard)