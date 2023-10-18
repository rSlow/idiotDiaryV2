from aiogram.fsm.state import StatesGroup, State


class MusicState(StatesGroup):
    start = State()


class MusicDownloadState(StatesGroup):
    wait_url = State()
    download = State()


class MusicEditState(StatesGroup):
    main = State()
    edit_image = State()
    edit_title = State()
    edit_artist = State()
    edit_album = State()
