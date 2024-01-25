from aiogram.fsm.state import StatesGroup, State


class INNParserFSM(StatesGroup):
    start = State()
    parse = State()
