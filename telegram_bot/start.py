import asyncio

from common.middlewares import DbSessionMiddleware
from common.storage import memory_storage
from config.bot import dp, bot
from common.ORM.database import Session
from config.logger import init_logging
from config.ui_config import set_ui_commands


async def main():
    dp.startup.register(init_logging)
    dp.update.middleware(DbSessionMiddleware(session_pool=Session))

    await memory_storage.set_all_states()

    await set_ui_commands(bot)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
