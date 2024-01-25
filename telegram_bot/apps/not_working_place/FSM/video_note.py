from aiogram.fsm.state import StatesGroup, State


class DownloadVideoNoteFSM(StatesGroup):
    main = State()
    download = State()
