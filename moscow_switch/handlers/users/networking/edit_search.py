from loader import dp, bot

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import search_kb
from states import Networking


@dp.callback_query_handler(text='edit_search', state=Networking.started)
async def settings(c: CallbackQuery, state: FSMContext):

    data = await state.get_data()

    text = 'Поиск\n'
    text += f'Возраст: \n   От: {data["age_min"]} \n    До: {data["age_max"]}' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
    text += f'Рост: \n   От: {data["len_min"]} \n    До: {data["len_max"]}' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
    text += f'Вес: \n   От: {data["weight_min"]} \n    До: {data["weight_max"]}' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''

    await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
    await c.message.answer(text=text, 
    reply_markup=search_kb)
    await Networking.started.set()


@dp.callback_query_handler(text='edit_len', state=Networking.started)
async def edit_len(c: CallbackQuery, state: FSMContext):

    await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
    await c.message.answer('Введите диапозон роста в формате: 110-180')
    await Networking.long.set()


@dp.message_handler(state=Networking.long)
async def lenght(message: Message, state: FSMContext):

    long = message.text.replace(' ', '').split('-')
    await state.update_data({'len_min': int(long[0]), 'len_max': int(long[1])})
    data = await state.get_data()

    text = 'Поиск\n'
    text += f'Возраст: \n   От: {data["age_min"]}\n   До: {data["age_max"]} \n' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
    text += f'Рост: \n  От: {data["len_min"]}\n   До: {data["len_max"]} \n' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
    text += f'Вес: \n   От: {data["weight_min"]}\n    До: {data["weight_max"]} \n' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(text=text, 
    reply_markup=search_kb)
    await Networking.started.set()



@dp.callback_query_handler(text='edit_age', state=Networking.started)
async def edit_age(c: CallbackQuery, state: FSMContext):

    await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
    await c.message.answer('Введите диапозон возрастов в формате: 25-30')
    await Networking.age.set()


@dp.message_handler(state=Networking.age)
async def age(message: Message, state: FSMContext):

    age = message.text.replace(' ', '').split('-')
    await state.update_data({'age_min': int(age[0]), 'age_max': int(age[1])})
    data = await state.get_data()

    text = 'Поиск\n'
    text += f'Возраст: \n   От: {data["age_min"]}\n   До: {data["age_max"]} \n' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
    text += f'Рост: \n  От: {data["len_min"]}\n   До: {data["len_max"]} \n' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
    text += f'Вес: \n   От: {data["weight_min"]}\n    До: {data["weight_max"]} \n' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(text=text, 
    reply_markup=search_kb)
    await Networking.started.set()


@dp.callback_query_handler(text='edit_weight', state=Networking.started)
async def edit_weight(c: CallbackQuery, state: FSMContext):

    await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
    await c.message.answer('Введите диапозон веса в формате: 70-120')
    await Networking.weight.set()


@dp.message_handler(state=Networking.weight)
async def weight(message: Message, state: FSMContext):

    weight = message.text.replace(' ', '').split('-')
    await state.update_data({'weight_min': int(weight[0]), 'weight_max': int(weight[1])})
    data = await state.get_data()

    text = 'Поиск\n'
    text += f'Возраст: \n   От: {data["age_min"]}\n   До: {data["age_max"]} \n' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
    text += f'Рост: \n  От: {data["len_min"]}\n   До: {data["len_max"]} \n' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
    text += f'Вес: \n   От: {data["weight_min"]}\n    До: {data["weight_max"]} \n' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''

    await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)
    await message.answer(text=text, 
    reply_markup=search_kb)
    await Networking.started.set()