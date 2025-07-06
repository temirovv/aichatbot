from aiogram.fsm.state import State, StatesGroup


class UserState(StatesGroup):
    lang = State()
    chat = State()


class AdminState(StatesGroup):
    admin = State()
