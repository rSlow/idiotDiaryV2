from abc import ABC, abstractmethod
from typing import Any


class ValidationError(AssertionError):
    pass


class BaseStateValidator(ABC):
    def __init__(self,
                 error_text: str | None):
        self.error_text = error_text

    @abstractmethod
    def validate(self, value: Any) -> Any:
        ...


class NameValidator(BaseStateValidator):
    def __init__(self):
        super().__init__(error_text="Неправильный формат имени. Попробуйте еще раз...")

    def validate(self, value: str) -> str:
        list_initials = value.split()
        if len(list_initials) == 0:
            raise ValidationError

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


class SumValidator(BaseStateValidator):
    def __init__(self):
        super().__init__(error_text="Неправильная форма суммы. Попробуйте еще раз...")

    def validate(self,
                 value: str) -> int | float:
        transfer_sum_edited = value.replace(",", ".")
        try:
            float_transfer_sum = round(float(transfer_sum_edited), 2)
            int_transfer_sum = int(float_transfer_sum)
            if float_transfer_sum == int_transfer_sum:
                return int_transfer_sum
            else:
                return float_transfer_sum
        except ValueError:
            raise ValidationError


class PhoneValidator(BaseStateValidator):
    def __init__(self):
        super().__init__(error_text="Неправильный формат номера. Попробуйте еще раз...")

    def validate(self, value: str) -> str:
        digits = list(filter(lambda v: v.isdigit(), value))

        try:
            if (digits[0] == "8" or digits[0] == "7") and len(digits) == 11:
                digits[0] = "+7"
            elif digits[0] == "9" and len(digits) == 10:
                digits.insert(0, "+7")
            else:
                raise ValidationError
        except IndexError:
            raise ValidationError

        return f"{digits[0]} " \
               f"({''.join(digits[1:4])})" \
               f" {''.join(digits[4:7])}" \
               f"-{''.join(digits[7:9])}" \
               f"-{''.join(digits[9:11])}"
