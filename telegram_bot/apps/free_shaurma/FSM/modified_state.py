from typing import Optional

from aiogram.fsm.state import StatesGroup, State

from common.base_keyboard import BaseKeyboardBuilder


class StateValidator:
    ...


class BankState(State):
    def __init__(self,
                 start_text: str,
                 start_keyboard: BaseKeyboardBuilder | None = None,
                 error_text: str | None = None,
                 error_keyboard: BaseKeyboardBuilder | None = None,

                 validators: list[StateValidator] | None = None,
                 state: str | None = None,
                 group_name: str | None = None):
        super().__init__(state=state, group_name=group_name)

        self.start_text = start_text
        self.start_keyboard = start_keyboard
        self.error_text = error_text
        self.error_keyboard = error_keyboard
        self.validators = validators


class BankStatesGroup(StatesGroup):
    @classmethod
    def first(cls) -> BankState:
        return cls.__all_states__[0]

    @classmethod
    def next(cls, state_obj: BankState | str | None = None) -> BankState | bool:
        if state_obj is None:
            return cls.first()

        state_str: str = state_obj.state if isinstance(state_obj, BankState) else state_obj

        for i, state in enumerate(cls.__all_states__):
            if state_str == state.state:
                if i + 1 == len(cls.__all_states__):
                    return False
                else:
                    return state
        else:
            raise AttributeError
