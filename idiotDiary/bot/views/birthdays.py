from datetime import date, timedelta

from idiotDiary.bot.di.jinja import JinjaRenderer
from idiotDiary.core.db import dto
from idiotDiary.core.db.dao.birthday import BirthdayDao
from idiotDiary.core.utils.dates import get_now


async def get_birthdays_message(
        dao: BirthdayDao, user_id: int, jinja: JinjaRenderer
):
    today = get_now().date()
    dates: dict[date, list[dto.Birthday]] = {}
    for i in range(4):
        fetch_date = today + timedelta(days=i)
        birthdays = await dao.get_by_date(user_id=user_id, d=fetch_date)
        if birthdays:
            dates[fetch_date] = birthdays

    return jinja.render_template(
        "birthdays/main_query.jinja2",
        dates=dates
    )
