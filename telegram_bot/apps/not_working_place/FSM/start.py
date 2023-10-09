from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    main = State()
