from aiogram.fsm.state import StatesGroup, State


class RegionSG(StatesGroup):
    start = State()
    set = State()
