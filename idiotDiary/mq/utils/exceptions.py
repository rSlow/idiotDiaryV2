from idiotDiary.core.utils.exceptions import BaseError


class PageError(BaseError):
    pass


class InvalidSubPageError(PageError):
    log_message = "Алярм! Невалидная страница при парсинге подписок - {page_url}. "


class CaptchaPageError(PageError):
    log_message = "Вылезло окно капчи. Возможно, требуется обновление куков."


class NoReelDownloadedError(BaseError):
    log_message = "Не найден скачанный файл"
