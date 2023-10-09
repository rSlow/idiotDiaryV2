from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from common.handlers import start, delete
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

# ----- HANDLERS ----- #
dp.message.register(
    start,
    Command("start")
)

dp.include_routers(root_router)

dp.message.register(delete)
