import logging
from typing import Iterable

from dishka import provide, Provider, Scope
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome import webdriver as chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from seleniumwire import webdriver
from seleniumwire.request import Request

from idiotDiary.bot.services.subs.url_factory import get_headers
from idiotDiary.mq.config.models.main import TaskiqAppConfig
from idiotDiary.mq.config.models.selenium import SeleniumConfig, SeleniumDriverType

logger = logging.getLogger(__name__)


def _driver_interceptor(request: Request):
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
        seleniumwire_options = {"auto_config": False}
        if config.proxy is not None:
            seleniumwire_options['proxy'] = {
                "http": config.proxy.uri,
                "https": config.proxy.uri,
                'no_proxy': 'localhost,127.0.0.1'
            }

        match config.type_:
            case SeleniumDriverType.REMOTE:
                driver = webdriver.Remote(
                    config.uri,
                    DesiredCapabilities.CHROME,
                    options=options, seleniumwire_options=seleniumwire_options
                )

            case SeleniumDriverType.CHROME:
                service = chrome.Service(executable_path=config.path)
                driver = webdriver.Chrome(
                    options=options, service=service, seleniumwire_options=seleniumwire_options
                )
                cdc_options = [
                    "cdc_adoQpoasnfa76pfcZLmcfl_Array",
                    "cdc_adoQpoasnfa76pfcZLmcfl_JSON",
                    "cdc_adoQpoasnfa76pfcZLmcfl_Object",
                    "cdc_adoQpoasnfa76pfcZLmcfl_Promise",
                    "cdc_adoQpoasnfa76pfcZLmcfl_Proxy",
                    "cdc_adoQpoasnfa76pfcZLmcfl_Symbol",
                    "cdc_adoQpoasnfa76pfcZLmcfl_Window",
                ]
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": ";".join([f"delete window.{value}" for value in cdc_options])
                })

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
                args = []
                [options.add_argument(arg) for arg in args]

            case _ as driver_type:
                raise TypeError(f"{driver_type} is not supported.")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) "
                             "Gecko/20100101 Firefox/84.0")

        return options
