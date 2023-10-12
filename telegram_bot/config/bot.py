from aiogram import Bot, Dispatcher

from common.handlers import router as common_router
from common.storage import memory_storage
from .router import root_router
from .settings import ENV

token = ENV.str("BOT_TOKEN")

bot = Bot(
    token=token,
    parse_mode="HTML"
)
dp = Dispatcher(
    storage=memory_storage
)

# ----- ROUTERS ----- #
dp.include_routers(root_router)
dp.include_routers(common_router)
