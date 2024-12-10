from idiotDiary.core.utils.exceptions import BaseError


class InvalidSubPageError(BaseError):
    log_message = "Алярм! Невалидная страница при парсинге подписок - {page_url}. "
