from aiogram.types import InlineKeyboardButton

from apps.music.factory import EyeD3EditCBFactory, EyeD3ActionsEnum
from common.keyboards.base import BaseInlineKeyboardBuilder


class EyeD3MainKeyboard(BaseInlineKeyboardBuilder):
    class Buttons:
        edit_title = InlineKeyboardButton(
            text="Название",
            callback_data=EyeD3EditCBFactory(
                action=EyeD3ActionsEnum.title,
            ).pack()
        )
        edit_artist = InlineKeyboardButton(
            text="Исполнитель",
            callback_data=EyeD3EditCBFactory(
                action=EyeD3ActionsEnum.artist,
            ).pack()
        )
        edit_album = InlineKeyboardButton(
            text="Альбом",
            callback_data=EyeD3EditCBFactory(
                action=EyeD3ActionsEnum.album,
            ).pack()
        )
        edit_photo = InlineKeyboardButton(
            text="Обложка",
            callback_data=EyeD3EditCBFactory(
                action=EyeD3ActionsEnum.thumbnail,
            ).pack()
        )
        export = InlineKeyboardButton(
            text="Сохранить 💾",
            callback_data="export"
        )

    row_width = (2, 2, 1)
    buttons_list = [
        [Buttons.edit_title,
         Buttons.edit_artist,
         Buttons.edit_album,
         Buttons.edit_photo],
        [Buttons.export]
    ]


class EyeD3BackToMainKeyboard(BaseInlineKeyboardBuilder):
    class Buttons:
        back = InlineKeyboardButton(
            text="Назад 🔙",
            callback_data="back_to_edit"
        )
        clear = InlineKeyboardButton(
            text="Очистить 🗑",
            callback_data="clear"
        )

    buttons_list = [
        Buttons.back,
        Buttons.clear,
    ]
