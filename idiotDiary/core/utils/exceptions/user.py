from .base import BaseError


class NoUserFound(BaseError):
    log_message = "Пользователь не найден."


class NoUsernameFound(NoUserFound):
    log_message = "По имени пользователя {username} пользователь не найден."


class MultipleUsernameFound(BaseError):
    log_message = ("По имени пользователя {username} "
                   "найдено несколько пользователей!")
