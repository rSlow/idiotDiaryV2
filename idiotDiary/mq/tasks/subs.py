import logging
from urllib.parse import urlparse

from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration as hd
from aiogram_dialog import BgManagerFactory, ShowMode
from dishka import FromDishka
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.mq.broker import broker
from idiotDiary.mq.di.inject import inject
from idiotDiary.mq.utils.exceptions import InvalidSubPageError

logger = logging.getLogger(__name__)


def _is_table_ads_exist(driver: WebDriver):
    try:
        driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
        return True
    except NoSuchElementException:
        return False


@broker.task
@inject
async def is_url_valid(url: str, driver: FromDishka[WebDriver]):
    driver.implicitly_wait(5)
    parsed_url = urlparse(url)
    driver.get(f"{parsed_url.scheme}://{parsed_url.netloc}")  # get session data
    driver.get(url)
    return _is_table_ads_exist(driver)


@broker.task
@inject
async def check_ads(
        url: str, user_id: int, sub_id: int,
        driver: FromDishka[WebDriver], bot: FromDishka[Bot], bg: FromDishka[BgManagerFactory],
        user_dao: FromDishka[UserDao], sub_dao: FromDishka[SubscriptionDao]
):
    driver.implicitly_wait(5)
    parsed_url = urlparse(url)
    driver.get(f"{parsed_url.scheme}://{parsed_url.netloc}")  # get session data
    driver.get(url)
    if not _is_table_ads_exist(driver):
        raise InvalidSubPageError(page_url=url)
    new_ads_block = driver.find_elements(By.CSS_SELECTOR, "*[data-accuracy=sse-bulletin-new]")
    if new_ads_block:
        user = await user_dao.get_by_id(user_id)
        sub = await sub_dao.get(sub_id)
        quoted_name = hd.quote(sub.name)
        text = f"Для подписки <a href='{url}'>{quoted_name}</a> появились новые предложения!"
        await bot.send_message(chat_id=user.tg_id, text=text, disable_web_page_preview=True)
        await bg.bg(bot, user.tg_id, user.tg_id).update({}, show_mode=ShowMode.DELETE_AND_SEND)
