from aiogram.fsm.state import StatesGroup, State


class MusicState(StatesGroup):
    start = State()


class YTDownloadState(StatesGroup):
    wait_url = State()
    download = State()


class EyeD3State(StatesGroup):
    wait_file = State()
    main = State()


class EyeD3EditState(StatesGroup):
    image = State()
    title = State()
    artist = State()
    album = State()
