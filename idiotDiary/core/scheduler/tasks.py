from datetime import timedelta

from aiogram import Bot
from aiogram_dialog import BgManagerFactory, ShowMode
from dishka import FromDishka

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.core.db.dao.birthday import BirthdayDao
from idiotDiary.core.db.dao.notification import UserNotificationDao
from idiotDiary.core.scheduler.context import SchedulerInjectContext
from idiotDiary.core.utils.dates import get_now


@SchedulerInjectContext.inject
async def send_birthdays(
        user_id: int,
        birthdays_dao: FromDishka[BirthdayDao],
        notification_dao: FromDishka[UserNotificationDao],
        user_dao: FromDishka[UserDao],
        jinja: FromDishka[JinjaRenderer],
        bot: FromDishka[Bot],
        bg: FromDishka[BgManagerFactory]
):
    user_state = await notification_dao.get_user_state(user_id)
    user = await user_dao.get_by_id(user_id)
    if user_state is None:
        user_state = await notification_dao.add_or_update_user_state(user_id)
    timeshift = timedelta(
        hours=user_state.timeshift.hour,
        minutes=user_state.timeshift.minute,
    )
    today = get_now().date() - timeshift

    today_birthdays = await birthdays_dao.get_by_date(today, user_id)
    tomorrow_birthdays = await birthdays_dao.get_by_date(
        today + timedelta(days=1), user_id
    )
    if today_birthdays or tomorrow_birthdays:
        message_text = jinja.render_template(
            "birthdays/schedule_birthdays.jinja2",
            today_birthdays=today_birthdays,
            tomorrow_birthdays=tomorrow_birthdays
        )
        await bot.send_message(chat_id=user.tg_id, text=message_text)
        await bg.bg(bot, user.tg_id, user.tg_id).update(
            {}, show_mode=ShowMode.DELETE_AND_SEND
        )
