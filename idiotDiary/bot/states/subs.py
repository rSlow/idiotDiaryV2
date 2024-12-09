from aiogram.fsm.state import StatesGroup, State

from idiotDiary.bot.utils.states_factory import FSMSingleFactory

SubsMainFSM = FSMSingleFactory("SubsMainFSM")
CurrentSubsFSM = FSMSingleFactory("CurrentSubsFSM")


class SubMenu(StatesGroup):
    main = State()
    name = State()
    frequency = State()
    delete = State()
