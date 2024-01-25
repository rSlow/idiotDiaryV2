TIME_FORMAT = "%H-%M"
TIME_RE_FORMAT = r"\d{1,2}-\d{1,2}"
TIME_STRING_FORMAT = "ЧЧ-ММ"

DATE_FORMAT = "%d-%m-%Y"
DATE_RE_FORMAT = r"\d{1,2}-\d{1,2}-\d{4}"
DATE_STRING_FORMAT = "ДД-ММ-ГГГГ"

DATETIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
DATETIME_RE_FORMAT = rf"{DATE_RE_FORMAT} {TIME_RE_FORMAT}"
DATETIME_STRING_FORMAT = f"{DATE_STRING_FORMAT} {TIME_STRING_FORMAT}"
