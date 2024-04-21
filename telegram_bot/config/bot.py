from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from aiogram_dialog import setup_dialogs

from apps.free_shaurma.handlers import test_fsh_router
from common.handlers.errors import error_router
from common.handlers.main import start_router, main_menu
from common.storage import redis_storage
from . import settings
from loguru import logger
from .router import apps_router
from .settings import ENV
from .startup_shutdown import on_startup, on_shutdown

token = ENV.str("BOT_TOKEN")

bot = Bot(
    token=token,
    parse_mode="HTML"
)
dp = Dispatcher(
    storage=redis_storage,
    events_isolation=SimpleEventIsolation()
)


def init_dispatcher(dispatcher: Dispatcher):
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)

    setup_dialogs(dispatcher)

    if settings.DEBUG:
        logger.info("SET DEBUG MODE")

        dispatcher.include_routers(
            test_fsh_router,
        )

    dispatcher.include_routers(
        start_router,
        error_router,
        main_menu,
        apps_router,
    )
