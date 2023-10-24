from aiogram.fsm.state import StatesGroup, State


class INNParser(StatesGroup):
    start = State()
    parse = State()
