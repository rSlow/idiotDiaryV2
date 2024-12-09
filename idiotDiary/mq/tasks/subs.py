from dishka import FromDishka
from dishka.integrations.telebot import inject
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from idiotDiary.mq.broker import broker


@broker.task
@inject
async def check_url(url: str, driver: FromDishka[WebDriver]):
    driver.get(url)
    driver.implicitly_wait(10)
    ads_table = driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
    if ads_table:
        return driver.current_url


@broker.task
@inject
async def check_ads(url: str, driver: FromDishka[WebDriver]):
    driver.get(url)
    driver.implicitly_wait(10)
    ads_table = driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
    if not ads_table:
        raise ...
    new_ads_block = driver.find_element(By.CSS_SELECTOR, "*[data-accuracy=sse-bulletin-new]")
    ...
