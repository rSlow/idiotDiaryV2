from abc import ABC, abstractmethod, abstractproperty
from typing import Any

from aiogram.types import KeyboardButton

from config import settings


class BaseButtonValidator(ABC):
    arg_name: str = abstractproperty

    @abstractmethod
    def validate(self, value: Any) -> Any:
        ...


class UserIDValidator(BaseButtonValidator):
    arg_name = "user_id"

    def __init__(self, user_id: int | str):
        super().__init__()

        self.user_id = str(user_id)

    def validate(self, value: str | int) -> Any:
        if value != str(self.user_id):
            return False
        return True


class IsOwnerValidator(BaseButtonValidator):
    arg_name = "user_id"

    def validate(self, value: str | int) -> Any:
        if str(value) != settings.OWNER_ID:
            return False
        return True


class ButtonWithValidator(KeyboardButton):
    def __init__(self, text: str, validator: BaseButtonValidator):
        super().__init__(text=text)
        self.validator = validator
