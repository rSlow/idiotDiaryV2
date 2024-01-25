from aiogram.fsm.state import StatesGroup, State


class ImagesZipFSM(StatesGroup):
    start = State()
    waiting = State()
    finish = State()
