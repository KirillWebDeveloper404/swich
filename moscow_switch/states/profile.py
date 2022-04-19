from aiogram.dispatcher.filters.state import State, StatesGroup


class Profile(StatesGroup):

    started = State()
    photo = State()
    name = State()
    age = State()
    act = State()
    profi = State()
    lenght = State()
    weight = State()