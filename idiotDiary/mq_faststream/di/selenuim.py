from typing import Iterable

from dishka import provide, Provider

from idiotDiary.mq.config.models.selenium import SeleniumConfig


class SeleniumProvider(Provider):
    @provide
    def get_selenium(
            self, config: SeleniumConfig, options: Options
    ) -> Iterable[webdriver.Remote]:
        webdriver = webdriver.Remote(
            config.uri,
            DesiredCapabilities.CHROME,
            options=options
        )
        yield webdriver
        webdriver.quit()

    def get_selenium_options(self) -> Options:
        options = webdriver.ChromeOptions()
        args = [
            "--headless",
            "window-size=1920x1080",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage"
        ]
        [options.add_argument(arg) for arg in args]
        return options
