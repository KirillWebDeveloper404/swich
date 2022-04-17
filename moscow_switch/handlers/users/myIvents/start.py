from loader import bot, dp

from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, \
    CallbackQuery

from sql import IventItem, ActPlace, UserStat, IventStatistic
from states import MyIvent


@dp.message_handler(Text(contains='мои мероприятия', ignore_case=True))
async def start(message: Message, state: FSMContext):
    await MyIvent.started.set()
    ivents = [el for el in IventItem.select().where(IventItem.users == message.from_user.id)]

    if len(ivents) > 0:
        await message.answer('Ваши мероприятия', reply_markup=ReplyKeyboardMarkup([
            [KeyboardButton('🔙Главное меню')]
        ], resize_keyboard=True))

    is_match = True
    for ivent in ivents:
        is_match = False
        place = ActPlace.get(ActPlace.id == ivent.place)

        await message.answer(text=f'{place.name}\n{place.desc}', reply_markup=InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='✅ Я уже посетил это место', callback_data=ivent.id),
            InlineKeyboardButton(text='Удалить', callback_data=ivent.id)
        ))

    if is_match:
        await state.finish()
        await message.answer('Вы еще не выбрали ни одного мероприятия. Вы можете выбрать мероприятие для себя в '
                             'разделе найти мероприятие')


@dp.callback_query_handler(state=MyIvent.started)
async def delete(c: CallbackQuery):
    ivent = IventItem.get(IventItem.id == c.data)

    user_stat = UserStat.get(UserStat.tg_id == c.from_user.id)
    user_stat.visit_now = str(int(user_stat.visit_now) + 1)
    user_stat.visit_future = str(int(user_stat.visit_future) - 1)
    user_stat.save()

    ivent_stat = IventStatistic.get(IventStatistic.place_id == ivent.place)
    ivent_stat.visit_future = str(int(ivent_stat.visit_future) - 1)
    ivent_stat.visit_now = str(int(ivent_stat.visit_now) + 1)
    ivent_stat.save()

    ivent.delete_instance()

    await bot.delete_message(chat_id=c.from_user.id, message_id=c.message.message_id)
