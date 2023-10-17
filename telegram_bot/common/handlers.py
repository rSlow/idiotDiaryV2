from aiogram import types, Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from config.logger import logger
from .FSM import CommonState
from .keyboards.base import BaseKeyboardBuilder
from .keyboards.start import StartKeyboard

first_router = Router()
last_router = Router()


@first_router.message(Command("start", "cancel"))
@first_router.message(F.text == BaseKeyboardBuilder.on_main_button_text)
async def start(message: types.Message, state: FSMContext, text: str | None = None):
    await state.set_state(CommonState.start)
    await message.answer(
        text=text or "Куда надо?",
        reply_markup=StartKeyboard.build(
            validator_args={"user_id": message.from_user.id}
        )
    )


@first_router.error(F.update.message.as_("message"))
async def key_error_pass(event: types.ErrorEvent, message: types.Message, state: FSMContext):
    data = await state.get_data()
    if isinstance(event.exception, KeyError) and not data:  # check if empty FSM data and KeyError exception
        await start(
            message=message,
            state=state,
            text=f"Бот был перезагружен, и промежуточные данные были утеряны. "
                 f"Попробуйте воспользоваться функцией еще раз."
        )
    else:
        await start(
            message=message,
            state=state,
            text=f"Извините, во время работы бота произошла ошибка. Мы вынуждены вернуть вас на главный экран. "
                 f"Попробуйте воспользоваться функцией еще раз."
        )
    logger.exception(event.exception)


@last_router.message(F.text)
async def delete(message: types.Message):
    await message.delete()
