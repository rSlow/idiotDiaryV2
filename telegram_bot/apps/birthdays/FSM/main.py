from aiogram.fsm.state import StatesGroup, State


class BirthdaysFSM(StatesGroup):
    main = State()
    clear_confirm = State()


class TimeCorrectionFSM(StatesGroup):
    start = State()
    set = State()


class BirthdaysNotificationFSM(StatesGroup):
    main = State()
    add_time = State()
    confirm_add_time = State()
    del_time = State()
    clear = State()
