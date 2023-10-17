from enum import Enum, EnumType

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


class TypeInterface:
    button_type = str | KeyboardButton | EnumType
    iterable = list[button_type] | tuple[button_type]
    double_iterable = list[iterable] | tuple[iterable]
    buttons_list_type = iterable | double_iterable


class BaseKeyboardBuilder(ReplyKeyboardBuilder):
    resize_keyboard: bool = True
    input_field_placeholder: str | None = None
    one_time_keyboard: bool | None = None
    is_persistent: bool | None = None
    selective: bool | None = None

    row_width: int | None = 2

    add_on_main_button: bool = True
    on_main_button_text: str = "На главную ◀"

    buttons_list: TypeInterface.buttons_list_type = []

    def _add_from_text(self, text: str):
        self.add(KeyboardButton(text=text))

    def as_markup(self):
        if self.buttons_list is None and not self.add_on_main_button:
            raise RuntimeError("buttons_list is not specified")
        else:
            self._process_buttons_list(self.buttons_list)

        if self.add_on_main_button:
            self._add_from_text(self.on_main_button_text)

        if self.row_width is not None:
            self.adjust(self.row_width)

        return super().as_markup(
            resize_keyboard=self.resize_keyboard,
            input_field_placeholder=self.input_field_placeholder,
            one_time_keyboard=self.one_time_keyboard,
            is_persistent=self.is_persistent,
            selective=self.selective
        )

    @classmethod
    def build(cls, *args, **kwargs):
        return cls(*args, **kwargs).as_markup()

    def _process_buttons_list(self, buttons_list: TypeInterface.buttons_list_type):

        def _prepare_row(buttons_row: TypeInterface.iterable):
            prepared_row: list[KeyboardButton] = []
            for button in buttons_row:
                if isinstance(button, str):
                    prepared_button = KeyboardButton(text=button)
                elif isinstance(button, Enum):
                    prepared_button = KeyboardButton(text=button.value)
                elif isinstance(button, KeyboardButton):
                    prepared_button = button
                else:
                    raise TypeError(f"button {button} is not matches to 'str', 'Enum' or 'KeyboardButton'")

                prepared_row.append(prepared_button)
            return prepared_row

        for row in buttons_list:
            if isinstance(row, (list, tuple)):
                self.row(*_prepare_row(row))
            elif isinstance(row, (str, KeyboardButton, Enum)):
                self.add(*_prepare_row(buttons_list))
                return


class CancelKeyboard(BaseKeyboardBuilder):
    pass
