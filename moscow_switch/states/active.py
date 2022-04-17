from aiogram.dispatcher.filters.state import State, StatesGroup


class ACT(StatesGroup):
    started = State()
    ivent = State()