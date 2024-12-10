from dishka import FromDishka
from dishka.integrations.taskiq import inject
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from idiotDiary.bot.views.alert import BotAlert
from idiotDiary.mq.broker import broker


@broker.task
@inject
async def check_url(url: str, driver: FromDishka[WebDriver]):
    driver.implicitly_wait(5)
    driver.get(url)
    ads_table = driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
    if ads_table:
        return driver.current_url


@broker.task
@inject
async def check_ads(url: str, driver: FromDishka[WebDriver], alert: FromDishka[BotAlert]):
    # wait = WebDriverWait(driver, 10)
    # wait.until()

    driver.implicitly_wait(5)
    driver.get(url)
    ads_table = driver.find_element(By.CSS_SELECTOR, "table.viewdirBulletinTable")
    if not ads_table:
        raise InvalidSubscriptionUrlError  # TODO
    new_ads_block = driver.find_elements(By.CSS_SELECTOR, "*[data-accuracy=sse-bulletin-new]")
    if bool(new_ads_block):
        await alert("Нашлась ссылка!")
    return bool(new_ads_block)
