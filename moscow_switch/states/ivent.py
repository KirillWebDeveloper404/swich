from aiogram.dispatcher.filters.state import State, StatesGroup


class Ivent(StatesGroup):

    started = State()
    kategory = State()
    places_group = State()
    places = State()
    networking = State()