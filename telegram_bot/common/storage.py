from typing import Any, Union, Type

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State as TState
from aiogram.fsm.storage.base import StorageKey, StateType
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage

from common.ORM.state_model import State
from config.settings import ENV


class ModifiedMemoryStorage(MemoryStorage):

    async def set_state(self,
                        key: StorageKey,
                        state: StateType = None,
                        also_to_db: bool = True
                        ) -> None:
        await super().set_state(
            key=key,
            state=state
        )
        if also_to_db:
            await State.set_user_state(
                chat_id=key.chat_id,
                user_id=key.user_id,
                bot_id=key.bot_id,
                state=state.state if isinstance(state, TState) else state
            )

    async def set_all_states(self, also_to_db: bool = True):
        users = await State.get_all_states()
        for user in users:
            storage_key = StorageKey(
                chat_id=user.chat_id,
                user_id=user.user_id,
                bot_id=user.bot_id,
            )
            await self.set_state(
                key=storage_key,
                state=user.state,
                also_to_db=also_to_db
            )


memory_storage = ModifiedMemoryStorage()
redis_storage = RedisStorage.from_url(ENV.str("REDIS_URL"))

ValueType = Union[int, str, float, bool, Type[None]]


async def get_category_data(
        state: FSMContext,
        category_key: str,
        category_default: Any,
):
    data = await state.get_data()
    category_data: dict[str, Any] = data.get(category_key, category_default)
    return category_data


async def set_category_value(
        state: FSMContext,
        category_key: str,
        category_default: Any,
        param: str,
        value: ValueType
):
    data = await state.get_data()
    category_data: dict[str, Any] = data.get(category_key, category_default)
    category_data[param] = value
    await state.update_data({category_key: category_data})
