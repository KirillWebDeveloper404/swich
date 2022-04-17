from loader import dp, bot

from aiogram.types import CallbackQuery, Message

from states import Profile
from sql import User
from .start import start


@dp.callback_query_handler(text='edit_photo', state=Profile.started)
async def photo(c: CallbackQuery):

    await Profile.photo.set()
    await c.message.answer('Пришлите фото профиля')


@dp.message_handler(content_types=['photo'], state=Profile.photo)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.photo = message.photo[-1].file_id
    user.save()

    await start(message=message)




@dp.callback_query_handler(text='edit_name', state=Profile.started)
async def name(c: CallbackQuery):

    await Profile.name.set()
    await c.message.answer('Пришлите новое имя')


@dp.message_handler(state=Profile.name)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.name = message.text
    user.save()

    await start(message=message)




@dp.callback_query_handler(text='edit_age', state=Profile.started)
async def name(c: CallbackQuery):

    await Profile.age.set()
    await c.message.answer('Пришлите новый возраст')


@dp.message_handler(state=Profile.age)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.age = message.text
    user.save()

    await start(message=message)




@dp.callback_query_handler(text='edit_act', state=Profile.started)
async def name(c: CallbackQuery):

    await Profile.act.set()
    await c.message.answer('Пришлите новый вид вашей деятельности')


@dp.message_handler(state=Profile.act)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.field_activity = message.text
    user.save()

    await start(message=message)




@dp.callback_query_handler(text='edit_len', state=Profile.started)
async def name(c: CallbackQuery):

    await Profile.lenght.set()
    await c.message.answer('Пришлите новый рост')


@dp.message_handler(state=Profile.lenght)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.length = message.text
    user.save()

    await start(message=message)




@dp.callback_query_handler(text='edit_weight', state=Profile.started)
async def name(c: CallbackQuery):

    await Profile.weight.set()
    await c.message.answer('Пришлите новый вес')


@dp.message_handler(state=Profile.weight)
async def set_photo(message: Message):

    user = User.get(User.tg_id == message.from_user.id)
    user.weight = message.text
    user.save()

    await start(message=message)
