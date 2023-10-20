from typing import Type, Optional, Any, Callable

from aiogram.fsm.state import StatesGroup, State

from apps.free_shaurma.validators import BaseStateValidator
from common.keyboards.base import BaseReplyKeyboardBuilder, CancelKeyboard


class BankState(State):
    def __init__(self,
                 start_text: str,
                 keyboard: Type[BaseReplyKeyboardBuilder] = CancelKeyboard,
                 validator: BaseStateValidator | Callable[[Any], Any] | None = None,
                 state: str | None = None,
                 group_name: str | None = None):
        super().__init__(state=state, group_name=group_name)

        self.start_text = start_text
        self.keyboard = keyboard
        self.validator = validator

    def next(self) -> Optional["BankState"]:
        group = self.group
        for i, state in enumerate(group.__all_states__):
            if self.state == state.state:
                if i + 1 == len(group.__all_states__):
                    return None
                else:
                    return group.__all_states__[i + 1]
        else:
            raise RuntimeError(f"can't find next state for state {self.state}")

    def validate(self, value: Any) -> Any:
        if self.validator is None:
            return value
        else:
            if isinstance(self.validator, BaseStateValidator):
                return self.validator.validate(value)
            elif callable(self.validator):
                return self.validator(value)
            else:
                raise RuntimeError("unknown validator type")


class BankStatesGroup(StatesGroup):
    @classmethod
    def first(cls) -> BankState:
        return cls.__all_states__[0]

    @classmethod
    def get_by_raw(cls, raw_state: str) -> BankState:
        for state in cls.__all_states__:
            if raw_state == state.state:
                return state
        else:
            raise KeyError
