import re

from idiotDiary.bot.utils.type_factory import regexp_factory


def frequency_validator(data: str):
    try:
        frequency = int(data)
    except ValueError:
        raise ValueError(f"Неверно указано значение частоты обновления - {data}")
    if frequency < 30:
        raise ValueError("Значение частоты обновления менее 30 секунд")
    return frequency


URLPattern = re.compile(r"https?://(www\.)?farpost\.ru/.+")
url_validator = regexp_factory(URLPattern)
