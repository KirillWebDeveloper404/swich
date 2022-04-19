from loader import dp, bot

from aiogram import types
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.storage import FSMContext

from states import Profile
from keyboards.inline import interes_kb, profi_kb
from sql import User
from .start import start, start_c


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
async def set_interes(c: types.CallbackQuery, state: FSMContext):
    data = {
        'sport': '❌',
        'walk': '❌',
        'osozn': '❌',
        'mistik': '❌',
        'money': '❌',
        'dance': '❌',
        'health': '❌',
        'alko': '❌',
        'musik': '❌',
        'moda': '❌',
    }

    await state.update_data(data)

    await Profile.act.set()
    await c.message.answer("Выбери что тебе интересно. Можно выбрать несколько или написать свой вариант.", reply_markup=interes_kb(data))


@dp.callback_query_handler(state=Profile.act)
async def set_interes_kb(c: types.CallbackQuery, state: FSMContext):
    if c.data == 'compleet':
        data = await state.get_data()
        data_text = {
            'sport': 'спорт',
            'walk': 'путешествия',
            'osozn': 'осознанность',
            'mistik': 'мистика',
            'money': 'финансы',
            'dance': 'тусовки',
            'health': 'ЗОЖ',
            'alko': 'винишко',
            'musik': 'музыка',
            'moda': 'мода',
        }

        text = ''

        for el in data:
            if data[el] == '✅':
                text += f'{data_text[el]}, '

        text = text[:-2]
        user = User.get(User.tg_id == c.from_user.id)
        user.field_activity = text
        user.save()
        await state.finish()
        await start_c(c=c)

    else:
        data = await state.get_data()
        data[c.data] = '✅' if data[c.data] == '❌' else '❌'
        await state.update_data(data)

        await c.message.edit_text(text="Выбери что тебе интересно. Можно выбрать несколько или написать свой вариант.", reply_markup=interes_kb(data))


@dp.message_handler(state=Profile.act)
async def activity(message: types.Message, state: FSMContext):
    text = message.text
    if len(text) > 10:

        user = User.get(User.tg_id == message.from_user.id)
        user.field_activity = text
        user.save()
        await state.finish()
        await start(message=message)

    else:
        data = await state.get_data()
        await Profile.act.set()
        await message.answer("Слишком коротко, напишите более подробно или выберите из предложенных", reply_markup=interes_kb(data))


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


@dp.callback_query_handler(text='edit_profi', state=Profile.started)
async def set_photo(c: types.CallbackQuery, state: FSMContext):    
    data = {
            'market': '❌',
            'konsalt': '❌',
            'bloger': '❌',
            'freelancer': '❌',
            'design': '❌',
            'shop': '❌',
            'buissnes': '❌',
            'iskustvo': '❌',
            'buti': '❌',
            'it': '❌',
            'psih': '❌',
            'eat': '❌',
            'stroy': '❌',
            'soc': '❌'
    }

    await state.update_data(data)

    await Profile.profi.set()
    await c.message.answer("Кем ты работаешь? Можно выбрать несколько вариантов или написать свой.", reply_markup=profi_kb(data))


@dp.callback_query_handler(state=Profile.profi)
async def set_profi_kb(c: types.CallbackQuery, state: FSMContext):
    if c.data == 'compleet':
        data = await state.get_data()
        data_text = {
            'market': 'Маркетинг',
            'konsalt': 'Консалтинг',
            'bloger': 'Блогер',
            'freelancer': 'Фрилансер',
            'design': 'Дизайн',
            'shop': 'Торговля',
            'buissnes': 'Предприниматель',
            'iskustvo': 'Творческий поиск',
            'buti': 'Бьюти',
            'it': 'Программист',
            'psih': 'Психолог',
            'eat': 'Рестораны',
            'stroy': 'Строительство',
            'soc': 'Соц работник'
        }

        text = ''

        for el in data:
            if data[el] == '✅':
                text += f'{data_text[el]}, '

        text = text[:-2]

        user = User.get(User.tg_id == c.from_user.id)
        user.profession = text
        user.save()

        data = {
            'sport': '❌',
            'walk': '❌',
            'osozn': '❌',
            'mistik': '❌',
            'money': '❌',
            'dance': '❌',
            'health': '❌',
            'alko': '❌',
            'musik': '❌',
            'moda': '❌',
        }
        await state.finish()
        await start_c(c=c)

    else:
        data = await state.get_data()
        data[c.data] = '✅' if data[c.data] == '❌' else '❌'
        await state.update_data(data)

        await c.message.edit_text(text="Кем ты работаешь? Можно выбрать несколько вариантов или написать свой.", reply_markup=profi_kb(data))


@dp.message_handler(state=Profile.profi)
async def set_interes(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.profession = message.text
    user.save()

    data = {
        'sport': '❌',
        'walk': '❌',
        'osozn': '❌',
        'mistik': '❌',
        'money': '❌',
        'dance': '❌',
        'health': '❌',
        'alko': '❌',
        'musik': '❌',
        'moda': '❌',
    }

    await state.update_data(data)
    await state.finish()
    await start(message=message)