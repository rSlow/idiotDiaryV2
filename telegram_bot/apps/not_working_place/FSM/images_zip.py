from aiogram.fsm.state import StatesGroup, State


class ImagesZip(StatesGroup):
    start = State()
    waiting = State()
    finish = State()
