from loader import dp, bot

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline import search_kb, profi_kb, interes_kb
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




@dp.callback_query_handler(text='profi', state=Networking.started)
async def set_photo(c: CallbackQuery, state: FSMContext):    
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

    await Networking.profi.set()
    await c.message.answer("Выбери профессии", reply_markup=profi_kb(data))


@dp.callback_query_handler(state=Networking.profi)
async def set_profi_kb(c: CallbackQuery, state: FSMContext):
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

        selected = []

        for el in data:
            try:
                if data[el] == '✅':
                    selected.append(data_text[el])
            except:
                pass

        await state.update_data({'profi': selected})

        text = 'Поиск\n'
        text += f'Возраст: \n   От: {data["age_min"]}\n   До: {data["age_max"]} \n' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
        text += f'Рост: \n  От: {data["len_min"]}\n   До: {data["len_max"]} \n' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
        text += f'Вес: \n   От: {data["weight_min"]}\n    До: {data["weight_max"]} \n' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''
        text += f'Профессия(-и): {selected}' if len(selected) > 0 else ''
        text += f'Интересы: {data["field_activity"]}' if len(data['field_activity']) > 0 else ''

        await c.message.answer(text=text, 
        reply_markup=search_kb)
        await Networking.started.set()        

    else:
        data = await state.get_data()
        data[c.data] = '✅' if data[c.data] == '❌' else '❌'
        await state.update_data(data)

        await c.message.edit_text(text="Выбери профессии", reply_markup=profi_kb(data))


@dp.callback_query_handler(text='interes', state=Networking.started)
async def set_interes(c: CallbackQuery, state: FSMContext):
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

    await Networking.field_activity.set()
    await c.message.answer("Выбери интересы", reply_markup=interes_kb(data))


@dp.callback_query_handler(state=Networking.field_activity)
async def set_interes_kb(c: CallbackQuery, state: FSMContext):
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

        selected = []

        for el in data:
            try:
                if data[el] == '✅':
                    selected.append(data_text[el])
            except:
                pass

        await state.update_data({'field_activity': selected})

        text = 'Поиск\n'
        text += f'Возраст: \n   От: {data["age_min"]}\n   До: {data["age_max"]} \n' if (data['age_min'] != 0 or data['age_max'] != 10000) else ''
        text += f'Рост: \n  От: {data["len_min"]}\n   До: {data["len_max"]} \n' if (data['len_min'] != 0 or data['len_max'] != 10000) else ''
        text += f'Вес: \n   От: {data["weight_min"]}\n    До: {data["weight_max"]} \n' if (data['weight_min'] != 0 or data['weight_max'] != 10000) else ''
        text += f'Профессия: {data["profi"]} \n' if len(data['profi']) else ''
        text += f'Интересы: {selected}' if len(selected) > 0 else ''

        await c.message.answer(text=text, 
        reply_markup=search_kb)
        await Networking.started.set()

    else:
        data = await state.get_data()
        data[c.data] = '✅' if data[c.data] == '❌' else '❌'
        await state.update_data(data)

        await c.message.edit_text(text="Выбери интересы", reply_markup=interes_kb(data))