from aiogram.fsm.state import StatesGroup, State

from common.FSM import FSMSingleFactory

MusicMainFSM = FSMSingleFactory("MusicMainFSM", "start")


class YTDownloadFSM(StatesGroup):
    url = State()
    timecode = State()


class EyeD3FSM(StatesGroup):
    wait_file = State()
    main = State()
    edit = State()
