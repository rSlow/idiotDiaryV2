from aiogram.fsm.state import StatesGroup, State


class FShStartSG(StatesGroup):
    device = State()
    from_bank = State()
    to_bank = State()
