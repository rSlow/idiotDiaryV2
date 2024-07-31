from enum import Enum


class EyeD3ActionsEnum(Enum):
    title = "Название"
    artist = "Исполнитель"
    album = "Альбом"
    thumbnail = "Обложка"


class EyeD3MessagesEnum(Enum):
    title = "Введите новое название песни..."
    artist = "Введите нового исполнителя..."
    album = "Введите новое название альбома..."
    thumbnail = "Ожидаю новую обложку для файла..."
