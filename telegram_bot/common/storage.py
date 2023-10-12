from aiogram.fsm.storage.base import StorageKey, StateType
from aiogram.fsm.storage.memory import MemoryStorage

from common.ORM.state_model import State
from aiogram.fsm.state import State as TState


class ModifiedMemoryStorage(MemoryStorage):

    async def set_state(self,
                        key: StorageKey,
                        state: StateType = None
                        ) -> None:
        await super().set_state(
            key=key,
            state=state
        )
        await State.set_user_state(
            chat_id=key.chat_id,
            user_id=key.user_id,
            bot_id=key.bot_id,
            state=state.state if isinstance(state, TState) else state
        )

    async def set_all_states(self):
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
            )


memory_storage = ModifiedMemoryStorage()
