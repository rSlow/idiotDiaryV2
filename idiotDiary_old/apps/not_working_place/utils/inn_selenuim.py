import time
from typing import Callable

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement

from common.utils.decorators import coro_timer, to_async_thread
from .. import settings
from ..factory.inn import INNSchema


class SeleniumTimeout(TimeoutError):
    pass


@coro_timer(40, exc=SeleniumTimeout)
@to_async_thread
def get_inn_selenium(data: INNSchema) -> str:
    options = webdriver.ChromeOptions()
    args = ['--headless', 'window-size=1920x1080', "--disable-gpu", "--no-sandbox", "--disable-dev-shm-usage"]
    [options.add_argument(arg) for arg in args]

    driver = webdriver.Remote(
        settings.SELENIUM_URL,
        DesiredCapabilities.CHROME,
        options=options
    )

