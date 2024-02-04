from typing import Any

from aiogram.fsm.context import FSMContext

from common.storage import set_category_value, get_category_data, ValueType


async def get_eyed3_data(state: FSMContext):
    return await get_category_data(
        state=state,
        category_key="eyed3_data",
        category_default={}
    )


async def get_eyed3_value(state: FSMContext,
                          key: str,
                          default: Any = None):
    eyed3_data = await get_eyed3_data(state=state)
    return eyed3_data.get(key, default)


async def set_eyed3_value(
        state: FSMContext,
        eyed3_key: str,
        value: ValueType
):
    await set_category_value(
        state=state,
        category_key="eyed3_data",
        category_default={},
        param=eyed3_key,
        value=value
    )
