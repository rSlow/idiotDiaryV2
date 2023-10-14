from aiogram import Bot

from common.jinja import render_template
from config import settings
from .ORM.birthdays import Birthday


async def send_birthdays(bot: Bot):
    today_birthdays = await Birthday.get_today_list()
    tomorrow_birthdays = await Birthday.get_tomorrow_list()
    if today_birthdays or tomorrow_birthdays:
        message_text = render_template(
            template_name="send_birthdays.jinja2",
            data={
                "today_birthdays": today_birthdays,
                "tomorrow_birthdays": tomorrow_birthdays
            }
        )
        await bot.send_message(
            chat_id=settings.OWNER_ID,
            text=message_text
        )
