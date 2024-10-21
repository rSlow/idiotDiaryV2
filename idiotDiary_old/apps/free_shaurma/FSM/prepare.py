from aiogram.fsm.state import StatesGroup, State


class FShStartFSM(StatesGroup):
    device = State()
    from_bank = State()
    to_bank = State()
