from aiogram import Router, F, types, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from common.context_message import ContextMessageManager
from common.keyboards.base import CancelKeyboard
from .main import start_nwp
from ..FSM.inn_parser import INNParserFSM
from ..FSM.start import NWPStartFSM
from ..filters.inn_filter import INNFilter, INNSchema
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..utils.inn_selenuim import get_inn_selenium, SeleniumTimeout
from ..utils.render import render_inn

inn_router = Router(name="inn")


@inn_router.message(
    NWPStartFSM.main,
    F.text == NotWorkingPlaceKeyboard.Buttons.inn_parse,
)
async def inn_parse_start(message: types.Message, state: FSMContext):
    await state.set_state(INNParserFSM.start)

    message_text = render_inn()
    await message.answer(
        text=message_text,
        reply_markup=CancelKeyboard.build(),
    )


@inn_router.message(
    INNParserFSM.start,
    INNFilter()
)
async def get_inn(message: types.Message,
                  state: FSMContext,
                  bot: Bot,
                  inn: INNSchema,
                  message_manager: type[ContextMessageManager]):
    await state.set_state(INNParserFSM.parse)
    async with message_manager(bot=bot,
                               state=state,
                               message_text="Поиск...",
                               keyboard=ReplyKeyboardRemove()):
        try:
            result_inn = await get_inn_selenium(data=inn)
            await start_nwp(
                text=f"ИНН - <code>{result_inn}</code>" if result_inn is not None else "Не найдено.",
                message=message,
                state=state
            )
        except SeleniumTimeout:
            await start_nwp(
                text="Запрос не может выполниться по независящим от бота причинам. "
                     "Возможно, причина в сайте налоговой. Задача отменена.",
                message=message,
                state=state
            )
