from aiogram.fsm.state import StatesGroup, State


class CommonFSM(StatesGroup):
    start = State()
