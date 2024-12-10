import logging
from typing import Iterable

from dishka import provide, Provider, Scope
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver as chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote import webdriver as remote
from selenium.webdriver.remote.webdriver import WebDriver

from idiotDiary.mq.config.models.main import TaskiqAppConfig
from idiotDiary.mq.config.models.selenium import (
    SeleniumConfig, SeleniumDriverType
)

logger = logging.getLogger(__name__)


class SeleniumProvider(Provider):
    scope = Scope.APP

    @provide
    def get_selenium_config(self, config: TaskiqAppConfig) -> SeleniumConfig:
        logger.info("Created Selenium config: \n" + str(config.selenium))
        return config.selenium

    @provide(scope=Scope.REQUEST)
    def get_selenium_driver(self, config: SeleniumConfig, options: Options) -> Iterable[WebDriver]:
        match config.type_:
            case SeleniumDriverType.REMOTE:
                driver = remote.WebDriver(
                    config.uri,
                    DesiredCapabilities.CHROME,
                    options=options
                )

            case SeleniumDriverType.CHROME:
                service = chrome.Service(executable_path=config.path)
                driver = chrome.WebDriver(options, service)

            case _ as driver_type:
                raise TypeError(f"{driver_type} is not supported.")
        yield driver
        driver.close()
        driver.quit()

    @provide
    def get_selenium_options(self, config: SeleniumConfig) -> Options:
        match config.type_:
            case SeleniumDriverType.REMOTE:
                options = Options()
                args = [
                    "--headless",
                    "window-size=1920x1080",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
                [options.add_argument(arg) for arg in args]

            case SeleniumDriverType.CHROME:
                options = chrome.Options()
                args = []  # TODO
                [options.add_argument(arg) for arg in args]

            case _ as driver_type:
                raise TypeError(f"{driver_type} is not supported.")

        return options
