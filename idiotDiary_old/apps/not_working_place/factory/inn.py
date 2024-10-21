from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ValidationError, AfterValidator, BeforeValidator


def validate_fio(fio: str):
    fio_list = fio.split()
    assert len(fio_list) == 3, f"FIO is not valid"
    return fio


def validate_passport(passport: str):
    passport_list = passport.split()
    assert len(passport_list) == 2, f"passport data {passport} is not valid"
    series, number = passport_list
    assert len(series) == 4, f"series of passport {series} is not valid"
    assert len(number) == 6, f"number of passport {number} is not valid"
    return series + number


def validate_date(raw_date: str | None):
    if raw_date is None:
        return raw_date
    datetime.strptime(raw_date, "%d.%m.%Y")
    return raw_date


FIOType = Annotated[str, AfterValidator(validate_fio)]
PassportType = Annotated[str, AfterValidator(validate_passport)]
DateType = Annotated[str, BeforeValidator(validate_date)]


class INNSchema(BaseModel):
    fio: FIOType
    passport: PassportType
    birthday: DateType
    date_passport: DateType | None = None


def inn_factory(text: str):
    lines = text.strip().split("\n")
    match len(lines):
        case 4:
            fio, passport, birthday, date_passport = lines
        case 3:
            fio, passport, birthday = lines
            date_passport = None
        case _:
            raise ValueError
    try:
        model = INNSchema(
            fio=fio,
            passport=passport,
            date_passport=date_passport,
            birthday=birthday
        )
        return model
    except ValidationError:
        raise ValueError
