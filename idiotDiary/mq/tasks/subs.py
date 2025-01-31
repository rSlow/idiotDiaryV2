import logging
from urllib.parse import urlparse

from aiogram import Bot
from aiogram.utils.text_decorations import html_decoration as hd
from dishka import FromDishka
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from idiotDiary.core.config import Paths
from idiotDiary.core.db.dao.subscription import SubscriptionDao
from idiotDiary.core.db.dao.user import UserDao
from idiotDiary.mq.broker import broker
from idiotDiary.mq.di.inject import inject
from idiotDiary.mq.utils.exceptions import InvalidSubPageError, CaptchaPageError
from idiotDiary.mq.utils.request_context import RequestContext

logger = logging.getLogger(__name__)


def _is_table_ads_exist(driver: WebDriver):
    try:
        driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
        return True
    except NoSuchElementException:
        return False


def _is_captcha_window(driver: WebDriver):
    try:
        driver.find_element(By.XPATH, "//h2[contains(text(),'Вы не робот?')]")
        return True
    except NoSuchElementException:
        return False


COOKIE_FILE = "farpost.pkl"


@broker.task(priority=5)
@inject
async def is_url_valid(url: str, driver: FromDishka[WebDriver], paths: FromDishka[Paths]):
    parsed_url = urlparse(url)
    driver.get(f"{parsed_url.scheme}://{parsed_url.netloc}")  # get session data
    with RequestContext(driver, paths.cookies_folder_path / COOKIE_FILE):
        driver.get(url)
        if _is_captcha_window(driver):
            raise CaptchaPageError
    return _is_table_ads_exist(driver)


@broker.task
@inject
async def check_ads(
        url: str, user_id: int, sub_id: int,
        driver: FromDishka[WebDriver], bot: FromDishka[Bot], user_dao: FromDishka[UserDao],
        sub_dao: FromDishka[SubscriptionDao], paths: FromDishka[Paths]
):
    parsed_url = urlparse(url)
    driver.get(f"{parsed_url.scheme}://{parsed_url.netloc}")  # get session data
    with RequestContext(driver, paths.cookies_folder_path / COOKIE_FILE):
        driver.get(url)
        if _is_captcha_window(driver):
            raise CaptchaPageError
        if not _is_table_ads_exist(driver):
            raise InvalidSubPageError(page_url=url)

    new_ads_block = driver.find_elements(By.CSS_SELECTOR, "*[data-accuracy=sse-bulletin-new]")
    if new_ads_block:
        user = await user_dao.get_by_id(user_id)
        sub = await sub_dao.get(sub_id)
        quoted_name = hd.quote(sub.name)
        text = f"Для подписки <a href='{url}'>{quoted_name}</a> появились новые предложения!"
        await bot.send_message(chat_id=user.tg_id, text=text, disable_web_page_preview=True)
