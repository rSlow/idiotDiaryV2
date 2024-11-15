from idiotDiary.core.utils.exceptions import BaseError
from idiotDiary.core.utils.exceptions.taskiq import TaskiqTaskError


class BigDurationError(BaseError):
    log_message = (
        "Видео, на которое вы отправили ссылку, идет более 10 минут. "
        "По техническим причинам на данный момент скачивание аудио "
        "более 10 минут невозможно."
    )


class DownloadAudioError(TaskiqTaskError):
    def __init__(self, error: BaseException):
        super().__init__(
            message="Ошибка скачивания аудио:",
            error=error,
            user_message="Произошла ошибка скачивания файла. Загрузка отменена."
        )
