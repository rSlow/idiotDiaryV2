from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    start = State()
    confirm_delete_birthdays = State()
