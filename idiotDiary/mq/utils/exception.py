import logging
from typing import Callable, Awaitable

from taskiq import TaskiqMiddleware, TaskiqMessage
from taskiq.result.v2 import TaskiqResult

ExceptionHandler = Callable[
    [BaseException, TaskiqMessage, TaskiqResult],
    Awaitable[None]
]

logger = logging.getLogger(__name__)


class ExceptionMiddleware(TaskiqMiddleware):
    def __init__(self):
        super().__init__()

        self._exc_handlers: dict[type[BaseException], ExceptionHandler] = {}

    def error_handler(self, exc_type: type[BaseException]):
        def wrapper(func: ExceptionHandler) -> ExceptionHandler:
            self._exc_handlers[exc_type] = func
            return func

        return wrapper

    def add_error_handler(
            self, exc_type: type[BaseException], handler: ExceptionHandler
    ) -> None:
        self._exc_handlers[exc_type] = handler

    async def on_error(
            self, message: TaskiqMessage, result: TaskiqResult,
            exception: BaseException,
    ) -> Awaitable[None] | None:
        exc_handler = self._exc_handlers.get(type(exception))
        if exc_handler is not None:
            return await exc_handler(exception, message, result)
