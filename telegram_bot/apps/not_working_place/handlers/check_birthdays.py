from datetime import datetime, timedelta, date

from aiogram import Router, F, types

from common.jinja import render_template
from config import settings
from ..FSM.start import Start
from ..ORM.birthdays import Birthday
from ..keyboards.main import NotWorkingPlaceKeyboard

birthday_router = Router(name="morph")


@birthday_router.message(
    Start.main,
    F.text == NotWorkingPlaceKeyboard.Buttons.check_birthdays,

)
async def check_birthdays(message: types.Message):
    today = datetime.now().astimezone(settings.TIMEZONE).date()
    dates: dict[date, list[Birthday]] = {}
    for i in range(4):
        check_date = today + timedelta(days=i)
        date_list = await Birthday.get_date_list(check_date)
        if date_list:
            dates[check_date] = date_list

    message_text = render_template(
        template_name="send_date_birthdays.jinja2",
        data={"dates": dates}
    )

    await message.answer(
        text=message_text,
    )
