from typing import AsyncIterable

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dishka import Provider, Scope, provide

from ..config.models.bot import BotConfig
from ..views.bot_alert import BotAlert
from ..views.jinja_filters import setup_jinja


class BotProvider(Provider):
    scope = Scope.APP

    @provide
    async def get_bot(self, bot_config: BotConfig) -> AsyncIterable[Bot]:
        async with Bot(  # TODO ??? __aenter__ not exists
                token=bot_config.token,
                default=DefaultBotProperties(
                    parse_mode=ParseMode.HTML,
                    allow_sending_without_reply=True,
                ),
        ) as bot:
            setup_jinja(bot)
            yield bot

    # TODO нужен ли alert?
    @provide
    async def bot_alert(self,
                        bot: Bot,
                        bot_config: BotConfig) -> BotAlert:
        return BotAlert(bot, bot_config.log_chat)
