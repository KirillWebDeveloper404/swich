from loader import dp, bot

from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram import types

from sql import ActPlace, IventItem, User, UserStat, IventStatistic
from states import ACT, Ivent, Anketa


@dp.message_handler(Text(contains='Актуальное на этой неделе', ignore_case=True))
async def start(message: Message):
    user = User.get(User.tg_id == message.from_user.id)

    if user.age == None:
        await message.answer("Похоже вы у нас в первый раз, заполните анкету о себе чтобы начать общаться с другими.")
        await message.answer("Пришлите ваше фото")
        await Anketa.photo.set()
        return 0

    await ACT.started.set()

    _ck_ = await message.answer('<code>Clearing keyboard...</code>', reply_markup=ReplyKeyboardRemove())
    await _ck_.delete()

    kb = InlineKeyboardMarkup(row_width=1)
    link = InlineKeyboardButton(text='Перейти в чат', url='https://vk.com/')
    places = InlineKeyboardButton(text='К мероприятиям', callback_data='to_ivents')
    main_menu = InlineKeyboardButton(text='🔙 Главное меню', callback_data='main_menu')
    kb.add(link, places, main_menu)

    await message.answer('Здесь ты можешь выбрать для себя мероприятие и посмотреть кто еще на него идет. \n' \
                         'Также у нас есть общий чат',
                         reply_markup=kb
                         )


@dp.callback_query_handler(text='to_ivents', state=ACT.started)
async def ivent_list(c: CallbackQuery, state: FSMContext):
    await ACT.ivent.set()

    places = [el for el in ActPlace.select()]

    for place in places:
        await c.message.answer(text=f'{place.name} \n{place.desc}',
                             reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                 InlineKeyboardButton(text='Я пойду', callback_data=f'{place.id}'))
                             )


@dp.callback_query_handler(state=ACT.ivent)
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
        ivent_stat.place = ActPlace.get(ActPlace.id == c.data).name
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


@dp.message_handler(content_types=['photo'], state=Anketa.photo)
async def set_photo(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.photo = message.photo[-1].file_id
    user.save()

    await Anketa.profi.set()
    await message.answer("Напиши о своей профессии, кем ты работаешь?", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.profi)
async def set_interes(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.profession = message.text
    user.save()

    await Anketa.field_activity.set()
    await message.answer("Напиши о своих интересах, чем ты увлекаешься?", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.field_activity)
async def activity(message: types.Message):
    text = message.text
    if len(text) > 10:

        user = User.get(User.tg_id == message.from_user.id)
        user.field_activity = text
        user.save()

        await Anketa.lenght.set()
        await message.answer("Какого вы роста(в см):")

    else:

        await Anketa.field_activity.set()
        await message.answer("Слишком коротко, напишите более подробно:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Anketa.lenght)
async def leng(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.length = message.text
    user.save()

    await Anketa.weight.set()
    await message.answer("Ваш вес:")


@dp.message_handler(state=Anketa.weight)
async def weight(message: types.Message):
    user = User.get(User.tg_id == message.from_user.id)
    user.weight = message.text
    user.save()

    await Anketa.age.set()
    await message.answer("Сколько вам лет:")


@dp.message_handler(state=Anketa.age)
async def age(message: types.Message, state: FSMContext):
    user = User.get(User.tg_id == message.from_user.id)
    user.age = message.text
    user.save()

    await ACT.started.set()

    _ck_ = await message.answer('<code>Clearing keyboard...</code>', reply_markup=ReplyKeyboardRemove())
    await _ck_.delete()

    kb = InlineKeyboardMarkup(row_width=1)
    link = InlineKeyboardButton(text='Перейти в чат', url='https://vk.com/')
    places = InlineKeyboardButton(text='К мероприятиям', callback_data='to_ivents')
    main_menu = InlineKeyboardButton(text='🔙 Главное меню', callback_data='main_menu')
    kb.add(link, places, main_menu)

    await message.answer('Здесь ты можешь выбрать для себя мероприятие и посмотреть кто еще на него идет. \n' \
                         'Также у нас есть общий чат',
                         reply_markup=kb
                         )
