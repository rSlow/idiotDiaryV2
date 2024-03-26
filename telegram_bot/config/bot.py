from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import SimpleEventIsolation
from common.storage import redis_storage
from .settings import ENV

token = ENV.str("BOT_TOKEN")

bot = Bot(
    token=token,
    parse_mode="HTML"
)
dp = Dispatcher(
    storage=redis_storage,
    events_isolation=SimpleEventIsolation()
)
