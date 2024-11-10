from aiogram.fsm.state import StatesGroup, State


class FshPickFormSG(StatesGroup):
    device = State()
    from_bank = State()
    to_bank = State()
