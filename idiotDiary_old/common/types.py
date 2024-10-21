from typing import Iterable
from typing import Any, Callable, Awaitable

from aiogram.types import TelegramObject

UserIDType = str | Iterable[str]
HandlerType = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]
