from aiogram.fsm.state import StatesGroup, State


class ConvertVoiceFSM(StatesGroup):
    start = State()
    convert = State()
