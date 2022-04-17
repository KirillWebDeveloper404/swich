from aiogram.dispatcher.filters.state import State, StatesGroup


class Tarif(StatesGroup):

    started = State()
    select = State()
    pay = State()