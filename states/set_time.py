from aiogram.dispatcher.filters.state import StatesGroup, State


class SetTime(StatesGroup):
    time = State()
    zone = State()
