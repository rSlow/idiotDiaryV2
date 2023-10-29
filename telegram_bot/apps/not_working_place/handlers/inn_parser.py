from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from common.jinja import render_template
from common.keyboards.base import CancelKeyboard
from .main import start_nwp
from ..FSM.inn_parser import INNParser
from ..FSM.start import Start
from ..filters.inn_filter import INNFilter, INNSchema
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..utils.inn_selenuim import get_inn_selenium, SeleniumTimeout

inn_router = Router(name="inn")


@inn_router.message(
    Start.main,
    F.text == NotWorkingPlaceKeyboard.Buttons.inn_parse,
)
async def inn_parse_start(message: types.Message, state: FSMContext):
    await state.set_state(INNParser.start)

    message_text = render_template(template_name="inn_parser_message.jinja2")
    await message.answer(
        text=message_text,
        reply_markup=CancelKeyboard.build(),
    )


@inn_router.message(
    INNParser.start,
    INNFilter()
)
async def get_inn(message: types.Message, state: FSMContext, inn: INNSchema):
    s_msg = await message.answer(
        text="Поиск...",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(INNParser.parse)

    try:
        result_inn = await get_inn_selenium(data=inn)
        await start_nwp(
            text=f"ИНН - <code>{result_inn}</code>" if result_inn is not None else "Не найдено.",
            message=message,
            state=state
        )
    except SeleniumTimeout:
        await start_nwp(
            text="Запрос не может выполниться по независящим от бота причинам. Возможно, причина в сайте налоговой. "
                 "Задача отменена.",
            message=message,
            state=state
        )
    finally:
        await s_msg.delete()
