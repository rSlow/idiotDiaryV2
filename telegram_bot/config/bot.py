from aiogram import Bot, Dispatcher

from common.handlers import first_router, last_router
from common.storage import memory_storage, redis_storage
from .router import apps_router
from .settings import ENV
from .startup_shutdown import on_startup, on_shutdown

token = ENV.str("BOT_TOKEN")

bot = Bot(
    token=token,
    parse_mode="HTML"
)
dp = Dispatcher(
    storage=redis_storage
)
dp.startup.register(on_startup)
dp.shutdown.register(on_shutdown)

dp.include_routers(
    first_router,
    apps_router,
    last_router
)
