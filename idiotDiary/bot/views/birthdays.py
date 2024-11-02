from collections import defaultdict
from datetime import date, timedelta

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.birthday import BirthdayDao
from idiotDiary.core.utils.dates import get_now


async def get_birthdays_message(
        dao: BirthdayDao, user_id: int, jinja: JinjaRenderer
):
    today = get_now().date()
    birthdays = await dao.get_between_dates(
        user_id=user_id, start_d=today, end_d=today + timedelta(days=3)
    )
    dates: dict[date, list[dto.Birthday]] = defaultdict(list)
    for birthday in birthdays:
        dates[birthday.date].append(birthday)

    return jinja.render_template(
        "birthdays/main_query.jinja2", dates=dates
    )
