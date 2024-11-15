from aiogram.fsm.state import StatesGroup, State

from idiotDiary.bot.utils.states_factory import FSMSingleFactory

MusicMainSG = FSMSingleFactory("MusicMainSG")


class YTDownloadSG(StatesGroup):
    url = State()
    timecode = State()


class Eyed3EditSG(StatesGroup):
    get_file = State()
    main = State()
    edit = State()
