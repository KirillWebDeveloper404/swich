from loader import dp, bot

from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from states import Ivent
from sql import User, IventItem


@dp.callback_query_handler(state=Ivent.networking)
async def start(c: CallbackQuery, state: FSMContext):
    try:

        data = await state.get_data()
        await state.update_data({'user': data['user']+1})
        data = await state.get_data()

        users = [el.users for el in IventItem.select().where(IventItem.place == c.data)]

        user_list = []

        for user in users:
            try:
                if int(user.tg_id) != int(c.from_user.id) and int(user.age) > 0:
                    user_list.append(User.get(User.tg_id == user))
            except:
                pass

        user = user_list[data['user']]

        info = f'#{user.tg_id}\n'
        info += f"Имя: {user.name} \n"
        info += f"Возраст: {user.age} \n"
        info += f"Вид деятельности: {user.profession} \n"
        info += f"Интересы: {user.field_activity} \n"
        info += f"Рост: {user.length} \n"
        info += f"Вес: {user.weight} \n"

        result_kb = InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text='👍 Интересно', callback_data='like')).add(
            InlineKeyboardButton(text='➡️ Показать ещё', callback_data=f'{c.data}')).add(
            InlineKeyboardButton(text='Главное меню', callback_data='main_menu'))

        try:
            await c.message.answer(text='clear kb', reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton('Главное меню')]
            ], resize_keyboard=True))
            await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id + 1)
            await bot.send_photo(chat_id=c.from_user.id, photo=user.photo, caption=info, reply_markup=result_kb)
        except:
            await c.message.answer(text=info, reply_markup=result_kb)
        await Ivent.networking.set()

    except Exception as e:
        pass