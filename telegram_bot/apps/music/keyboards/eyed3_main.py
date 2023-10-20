from aiogram.types import InlineKeyboardButton

from common.keyboards.base import BaseInlineKeyboardBuilder


class EyeD3MainKeyboard(BaseInlineKeyboardBuilder):
    class Buttons:
        edit_title = InlineKeyboardButton(
            text="Название",
            callback_data="edit_title"
        )
        edit_artist = InlineKeyboardButton(
            text="Исполнитель",
            callback_data="edit_artist"
        )
        edit_album = InlineKeyboardButton(
            text="Альбом",
            callback_data="edit_album"
        )
        export = InlineKeyboardButton(
            text="Сохранить 💾",
            callback_data="export"
        )

    row_width = (2, 1, 1)
    buttons_list = [
        [Buttons.edit_title,
         Buttons.edit_artist,
         Buttons.edit_album],
        [Buttons.export]
    ]


class EyeD3BackToMainKeyboard(BaseInlineKeyboardBuilder):
    class Buttons:
        back = InlineKeyboardButton(
            text="Назад 🔙",
            callback_data="back_to_edit"
        )

    buttons_list = [
        Buttons.back,
    ]
