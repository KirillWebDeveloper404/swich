from aiogram.dispatcher.filters.state import State, StatesGroup


class ADS(StatesGroup):

    name = State()
    phone = State()
    address = State()
    link = State()
    desc = State()