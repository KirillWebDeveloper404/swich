from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from sql import PlacesGroup, Kategory, Place, IventItem, IventStatistic, UserStat, User
from states import Ivent


@dp.message_handler(state=Ivent.kategory)
async def curs_list(message: types.Message, state: FSMContext):
    kategory = Kategory.get(Kategory.name == message.text)

    await Ivent.places_group.set()

    places_group = [el.name for el in PlacesGroup.select().where(PlacesGroup.kategory == kategory.id)]
    keyboard = []

    for el in places_group:
        keyboard.append([KeyboardButton(el)])

    keyboard.append([KeyboardButton('Назад')])

    await message.answer(text='Выберем направление',
                         reply_markup=ReplyKeyboardMarkup(keyboard,
                                                          resize_keyboard=True)
                         )


@dp.message_handler(state=Ivent.places, text='Назад')
async def curs_list(message: types.Message, state: FSMContext):
    data = await state.get_data()

    await Ivent.places_group.set()

    places_group = [el.name for el in PlacesGroup.select().where(PlacesGroup.kategory == data['group_id'])]
    keyboard = []

    for el in places_group:
        keyboard.append([KeyboardButton(el)])

    keyboard.append([KeyboardButton('Назад')])

    await message.answer(text='Выберем тип мероприятия',
                         reply_markup=ReplyKeyboardMarkup(keyboard,
                                                          resize_keyboard=True)
                         )


@dp.message_handler(state=Ivent.places_group)
async def curs_list(message: types.Message, state: FSMContext):
    group = PlacesGroup.get(PlacesGroup.name == message.text)

    await Ivent.places.set()
    await state.update_data({'group_id': group.kategory})
    await message.answer("Выберите куда хотите пойти:", reply_markup=ReplyKeyboardMarkup([
        [KeyboardButton('Назад')]
    ], resize_keyboard=True))

    places = [el for el in Place.select().where(Place.group == group.id)]
    texts = []

    for el in places:
        texts.append(el)

    for i, text in enumerate(texts):
        mess = f'{text.name}\n{text.desc}' if text.name != text.desc else f'{text.name}'
        await message.answer(text=mess,
                            #  reply_markup=InlineKeyboardMarkup(row_width=1).add(
                            #      InlineKeyboardButton(text='Я пойду', callback_data=f'{text.id}'))
                             )


@dp.callback_query_handler(state=Ivent.places)
async def select_place(c: CallbackQuery, state: FSMContext):
    await Ivent.networking.set()
    await state.update_data({'user': -1})

    ivent = IventItem()
    ivent.users = c.from_user.id
    ivent.place = str(c.data)
    ivent.save()

    try:
        user_stat = UserStat.get(UserStat.tg_id == c.from_user.id)
        user_stat.visit_future = str(int(user_stat.visit_future) + 1)
        user_stat.save()
    except:
        user = User.get(User.tg_id == c.from_user.id)
        user_stat = UserStat()
        user_stat.tg_id = c.from_user.id
        user_stat.name = user.name
        user_stat.phone = user.phone
        user_stat.visit_now = 0
        user_stat.visit_future = 1
        user_stat.save()

    try:
        ivent_stat = IventStatistic.get(IventStatistic.place_id == c.data)
        ivent_stat.visit_future = str(int(ivent_stat.visit_future) + 1)
        ivent_stat.save()
    except:
        ivent_stat = IventStatistic()
        ivent_stat.place_id = c.data
        ivent_stat.place = Place.get(Place.id == c.data).name
        ivent_stat.visit_now = 0
        ivent_stat.visit_future = 1
        ivent_stat.save()

    users = [el.users for el in IventItem.select().where(IventItem.place == c.data)]
    users_list = []

    for user in users:
        if str(user) != str(c.from_user.id):
            users_list.append(user)

    if len(users_list) > 0:
        await c.message.answer(
            f"На это мероприятие собираются пойти еще {len(users_list)} человек. \nВы можете обьедениться и пойти "
            f"вместе. Показать список?",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton(text='Показать кто еще собирается на мероприятие', callback_data=f"{c.data}")
            ).add(
                InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
            ))
    else:
        await c.message.answer(f"Кроме вас на это мероприятие больше никто не идет",
                               reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                   InlineKeyboardButton(text='Главное меню', callback_data='main_menu')
                               ))
