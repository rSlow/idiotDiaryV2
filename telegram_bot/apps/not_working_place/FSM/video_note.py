from aiogram.fsm.state import StatesGroup, State


class DownloadVideoNote(StatesGroup):
    main = State()
    download = State()
