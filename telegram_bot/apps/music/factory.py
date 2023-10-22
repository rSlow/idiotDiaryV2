from enum import Enum

from aiogram.filters.callback_data import CallbackData


class EyeD3ActionsEnum(Enum):
    title = "title"
    artist = "artist"
    album = "album"
    thumbnail = "thumbnail"


class EyeD3MessagesEnum(Enum):
    title = "Введите новое название песни..."
    artist = "Введите нового исполнителя..."
    album = "Введите новое название альбома..."
    thumbnail = "Ожидаю новую обложку для файла..."


class EyeD3EditCBFactory(CallbackData, prefix="eyed3_edit"):
    action: EyeD3ActionsEnum
