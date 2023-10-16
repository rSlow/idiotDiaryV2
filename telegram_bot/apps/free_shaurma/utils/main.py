from .. import settings
from datetime import datetime
# import pytz


def grade(number: str):
    found = number.find(",")

    if ~found:  # found
        integer = number[:found]
        fractional = number[found:]
    else:
        integer = number
        fractional = ""
    graded_number = ""
    for i, sym in enumerate(integer[::-1], 1):
        graded_number = sym + graded_number
        if i % 3 == 0:
            graded_number = " " + graded_number

    graded_number = graded_number.strip() + fractional
    return graded_number


def strike(text):
    sym = u'\u0336'
    stroked = ""
    for i in text:
        stroked += (i + sym)
    return stroked


def get_render_func(bank, on_bank, device):
    return settings.BANKS[bank]["on_banks"][on_bank][device]


def get_now():
    # tz = pytz.timezone("Asia/Vladivostok")
    # return datetime.now().astimezone(tz=tz)
    return datetime.now()
