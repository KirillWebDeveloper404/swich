from loader import dp, bot

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from keyboards.inline import result_kb, search_kb
from states import Networking
from sql import User


@dp.callback_query_handler(text='search', state=Networking.started)
async def start(c: CallbackQuery, state: FSMContext):
    try:

        await state.update_data({'user': 0})
        data = await state.get_data()

        users = [el for el in User.select()]

        user_list = []

        for user in users:
            try:
                if (data['age_min'] <= int(user.age) <= data['age_max']) and (
                        data['weight_min'] <= int(user.weight) <= data['weight_max']) and (
                        data['len_min'] <= int(user.length) <= data['len_max']):
                    if str(user.tg_id) != str(c.from_user.id):
                        user_list.append(user)
            except:
                pass
            
        user = user_list[data['user']]

        info = f'#{user.tg_id}\n'
        info += f"Имя: {user.name} \n"
        info += f"Возраст: {user.age} \n"
        info += f"Интересы: {user.field_activity} \n"
        info += f"Рост: {user.length} \n"
        info += f"Вес: {user.weight} \n"

        try:
            await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
            await c.message.answer(text='clear kb', reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id + 1)
            await bot.send_photo(chat_id=c.from_user.id, photo=user.photo, caption=info, reply_markup=result_kb)
        except Exception as e:
            await c.message.answer(text=info, reply_markup=result_kb)
        await Networking.started.set()

    except Exception as e:
        print(e)
        data = {
            'age_min': 0,
            'len_min': 0,
            'age_max': 10000,
            'len_max': 10000,
            'weight_min': 0,
            'weight_max': 10000
        }

        await state.update_data(data)

        await c.message.answer(
            'К сожалению по вашему запросу никого не удалось найти. Попробуйте перенастроить фильтры',
            reply_markup=search_kb)


@dp.callback_query_handler(text='next', state=Networking.started)
async def next(c: CallbackQuery, state: FSMContext):
    try:

        data = await state.get_data()
        await state.update_data({'user': data['user'] + 1})
        data = await state.get_data()

        users = [el for el in User.select()]

        user_list = []

        for user in users:
            if (data['age_min'] < int(user.age) < data['age_max']) and (
                    data['weight_min'] < int(user.weight) < data['weight_max']) and (
                    data['len_min'] < int(user.length) < data['len_max']):
                if str(user.tg_id) != str(c.from_user.id):
                    user_list.append(user)

        user = user_list[data['user']]

        info = f'#{user.tg_id}\n'
        info += f"Имя: {user.name} \n"
        info += f"Возраст: {user.age} \n"
        info += f"Вид деятельности: {user.profession} \n"
        info += f"Интересы: {user.field_activity} \n"
        info += f"Рост: {user.length} \n"
        info += f"Вес: {user.weight} \n"

        try:
            await c.message.answer(text='clear kb', reply_markup=ReplyKeyboardRemove())
            await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id + 1)
            await bot.send_photo(chat_id=c.from_user.id, photo=user.photo, caption=info, reply_markup=result_kb)
        except Exception as e:
            await c.message.answer(text=info, reply_markup=result_kb)
        await Networking.started.set()

    except Exception as e:
        data = {
            'age_min': 0,
            'len_min': 0,
            'age_max': 10000,
            'len_max': 10000,
            'weight_min': 0,
            'weight_max': 10000
        }

        await state.update_data(data)

        await c.message.answer(
            'К сожалению по вашему запросу никого не удалось найти. Попробуйте перенастроить фильтры',
            reply_markup=search_kb)
