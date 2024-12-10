import logging
from typing import Iterable

from dishka import provide, Provider, Scope
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver as chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumwire import webdriver

from idiotDiary.bot.services.subs.url_factory import get_headers
from idiotDiary.mq.config.models.main import TaskiqAppConfig
from idiotDiary.mq.config.models.selenium import SeleniumConfig, SeleniumDriverType

logger = logging.getLogger(__name__)


def _driver_interceptor(request):
    for header, value in get_headers().items():
        request.headers[header] = value


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
                driver = webdriver.Remote(
                    config.uri,
                    DesiredCapabilities.CHROME,
                    seleniumwire_options={"auto_config": False},
                    options=options
                )

            case SeleniumDriverType.CHROME:
                service = chrome.Service(executable_path=config.path)
                driver = webdriver.Chrome(options=options, service=service)

            case _ as driver_type:
                raise TypeError(f"{driver_type} is not supported.")

        driver.request_interceptor = _driver_interceptor
        yield driver

        driver.close()
        driver.quit()

    @provide
    def get_selenium_options(self, config: SeleniumConfig) -> Options:
        match config.type_:
            case SeleniumDriverType.REMOTE:
                options = webdriver.ChromeOptions()
                args = [
                    "--headless",
                    "window-size=1920x1080",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
                [options.add_argument(arg) for arg in args]

            case SeleniumDriverType.CHROME:
                options = webdriver.ChromeOptions()
                args = [
                    "window-size=1920x1080",
                    # "--headless",
                    # "--blink-settings=imagesEnabled=false",
                ]
                [options.add_argument(arg) for arg in args]

            case _ as driver_type:
                raise TypeError(f"{driver_type} is not supported.")

        return options
