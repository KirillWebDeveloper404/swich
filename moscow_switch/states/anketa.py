from aiogram.dispatcher.filters.state import State, StatesGroup


class Anketa(StatesGroup):

    photo = State()
    profi = State()
    name = State()
    phone = State()
    lenght = State()
    weight = State()
    age = State()
    field_activity = State()