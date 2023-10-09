from aiogram.fsm.state import StatesGroup, State


class ConvertVoice(StatesGroup):
    start = State()
    convert = State()
