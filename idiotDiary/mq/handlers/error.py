import logging

from aiogram.exceptions import TelegramForbiddenError
from aiogram.utils.markdown import html_decoration as hd
from dishka import FromDishka
from taskiq import TaskiqMessage

from idiotDiary.bot.views.alert import BotAlert
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.core.scheduler.scheduler import ApScheduler
from idiotDiary.mq.di.inject import error_inject
from idiotDiary.mq.utils.exception import ExceptionMiddleware

exc_middleware = ExceptionMiddleware()

logger = logging.getLogger(__name__)


@exc_middleware.error_handler(TelegramForbiddenError)
@error_inject
async def tg_user_blocked(
        exc: TelegramForbiddenError, _, __,
        user_dao: FromDishka[UserDao], subs_dao: FromDishka[SubscriptionDao],
        scheduler: FromDishka[ApScheduler]
):
    user_id: int = exc.method.chat_id
    await user_dao.deactivate(user_id)
    logger.info(f"Deactivated user with id {user_id}")

    user_subs = await subs_dao.get_active_user_subscriptions(user_id)
    for sub in user_subs:
        scheduler.remove_ad_subscription(sub.id_)
    await subs_dao.deactivate_user_subscriptions(user_id)


@exc_middleware.error_handler(Exception)
@error_inject
async def base_error(exc: Exception, message: TaskiqMessage, _, alert: FromDishka[BotAlert]):
    exc_text = (
        f"Получено исключение в taskiq, задача {message.task_name}:\n"
        f"-----\n"
        f"{str(exc)}"
    )
    logger.exception(exc_text, exc_info=exc)
    await alert(exc_text % hd.quote(str(exc)))
