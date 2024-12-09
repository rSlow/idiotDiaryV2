from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram_dialog import BgManagerFactory, ShowMode
from dishka import FromDishka
from taskiq import AsyncTaskiqTask, TaskiqResult, TaskiqResultTimeoutError

from idiotDiary.bot.views.alert import BotAlert
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.core.scheduler.context import SchedulerInjectContext
from idiotDiary.core.utils.dates import get_now
from idiotDiary.mq.tasks.subs import check_ads


@SchedulerInjectContext.inject
async def check_subscription(
        subscription_id: int,
        subs_dao: FromDishka[SubscriptionDao],
        user_dao: FromDishka[UserDao],
        bot: FromDishka[Bot],
        bg: FromDishka[BgManagerFactory],
        alert: FromDishka[BotAlert]
):
    sub = await subs_dao.get(subscription_id)
    user = await user_dao.get_by_id(sub.user_id)
    try:
        check_timestamp = get_now().timestamp()
        request_url = str(sub.url) + f"&date_created_min={check_timestamp}"
        task: AsyncTaskiqTask = await check_ads.kiq(url=request_url)
        res: TaskiqResult = await task.wait_result(timeout=240)
        if res.is_err:
            ...
        if res.return_value is True:
            quoted_name = hd.quote(sub.name)
            text = (f"Для подписки <a href='{request_url}'>{quoted_name}</a>"
                    f" появились новые предложения!")
            await bot.send_message(chat_id=user.tg_id, text=text, disable_web_page_preview=True)
            await bg.bg(bot, user.tg_id, user.tg_id).update({}, show_mode=ShowMode.DELETE_AND_SEND)

    except TaskiqResultTimeoutError:
        ...
