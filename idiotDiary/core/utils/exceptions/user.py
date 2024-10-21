from .base import BaseError


class NoUsernameFound(BaseError):
    log_message = "По этому username ничего не найдено"

    def __init__(self, username: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.username = username


class MultipleUsernameFound(BaseError):
    log_message = "По этому username найдено несколько пользователей!"

    def __init__(self, username: str | None = None, **kwargs) -> None:
        super().__init__(**kwargs)
        self.username = username
