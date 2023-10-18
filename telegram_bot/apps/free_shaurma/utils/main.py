import pytz

from datetime import datetime


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
