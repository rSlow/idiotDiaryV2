from aiogram import Dispatcher, BaseMiddleware
from aiogram_dialog.api.entities import DIALOG_EVENT_NAME

from .context_data import ContextDataMiddleware
from .logging import EventLoggingMiddleware


def setup_middlewares(dp: Dispatcher):
    _base_setup_middleware(dp, ContextDataMiddleware())
    _base_setup_middleware(dp, EventLoggingMiddleware())


def _base_setup_middleware(dp: Dispatcher, middleware: BaseMiddleware):
    dp.message.middleware(middleware)
    dp.business_message.middleware(middleware)
    dp.callback_query.middleware(middleware)

    update_handler = dp.observers[DIALOG_EVENT_NAME]
    update_handler.middleware(middleware)
