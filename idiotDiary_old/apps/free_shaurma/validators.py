from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class BaseTypeFactory(Protocol):
    error_text: str | None = None

    @abstractmethod
    def __call__(self, text: str) -> Any:
        ...


class NameTypeFactory(BaseTypeFactory):
    error_text = "Неправильный формат имени. Попробуйте еще раз..."

    def __call__(self, text: str) -> str:
        list_initials = text.split()
        if len(list_initials) == 0:
            raise ValueError

        last_initial = list_initials[-1]
        first_initials = list_initials[:-1]

        if len(last_initial) == 1:
            if last_initial.isalpha():
                last_initial += "."

        elif len(last_initial) > 2:
            last_initial = last_initial[0] + "."

        initials = first_initials + [last_initial]
        validated_name = " ".join(initials)
        return validated_name


class SumTypeFactory(BaseTypeFactory):
    error_text = "Неправильный формат суммы. Попробуйте еще раз..."

    def __call__(self, text: str) -> int | float:
        transfer_sum_edited = text.replace(",", ".")
        float_transfer_sum = round(float(transfer_sum_edited), 2)
        int_transfer_sum = int(float_transfer_sum)
        if float_transfer_sum == int_transfer_sum:
            return int_transfer_sum
        else:
            return float_transfer_sum


class PhoneTypeFactory(BaseTypeFactory):
    error_text = "Неправильный формат телефона. Попробуйте еще раз..."

    def __call__(self, text: str) -> str:
        digits = list(filter(lambda v: v.isdigit(), text))

        try:
            if (digits[0] == "8" or digits[0] == "7") and len(digits) == 11:
                digits[0] = "+7"
            elif digits[0] == "9" and len(digits) == 10:
                digits.insert(0, "+7")
            else:
                raise ValueError
        except IndexError:
            raise ValueError

        return f"{digits[0]} " \
               f"({''.join(digits[1:4])})" \
               f" {''.join(digits[4:7])}" \
               f"-{''.join(digits[7:9])}" \
               f"-{''.join(digits[9:11])}"
