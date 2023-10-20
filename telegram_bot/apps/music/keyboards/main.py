from common.keyboards.base import BaseReplyKeyboardBuilder


class MusicMainKeyboard(BaseReplyKeyboardBuilder):
    class Buttons:
        edit_music = "Редактор eyeD3 👁‍🗨"
        download_from_yt = "Скачать музыку из видео ⬇️"

    buttons_list = [
        Buttons.edit_music,
        Buttons.download_from_yt,
    ]
