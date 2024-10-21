from abc import ABC

from aiogram import types as t
from aiogram_dialog import ShowMode

from idiotDiary.core.utils.exceptions.base import BaseError


class UserNotifyException(Exception, ABC):
    """
    Базовый класс исключения для отправки сообщения пользователю.
    """

    message_text: str = "Оповещение"
    show_mode: ShowMode = ShowMode.DELETE_AND_SEND

    def __init__(self, **kwargs):
        self.map_kwargs = kwargs

    @property
    def message(self):
        return self.message_text.format_map(self.map_kwargs)


class EventTypeError(BaseError):
    log_message = "Ошибка типа события: {event_name}"

    def __init__(self, event: t.TelegramObject, **kwargs):
        super().__init__(event_name=event.__class__.__name__, **kwargs)


class UnknownEventTypeError(EventTypeError):
    log_message = "Неподдерживаемый тип события: {event_name}"


class PassEventException(EventTypeError):
    log_message = "Тип события {event_name} исключен из обработки."


class UnknownContentTypeError(BaseError):
    log_message = "Неизвестный тип контента: {file_content_type}"
