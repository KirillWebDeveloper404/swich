from aiogram.dispatcher.filters.state import State, StatesGroup


class Networking(StatesGroup):
    started = State()
    long = State()
    weight = State()
    age = State()
    field_activity = State()
    profi = State()
