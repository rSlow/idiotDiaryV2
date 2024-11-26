from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput

from idiotDiary.bot.schemas.inn import INNSchema, inn_factory
from idiotDiary.bot.states.not_working_place import INNParserSG
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.bot.views import buttons as b
from idiotDiary.bot.views.types import JinjaTemplate
from idiotDiary.mq.tasks.inn import get_inn


async def inn_handler(message: types.Message, __, manager: DialogManager, data: INNSchema):
    await manager.show(show_mode=ShowMode.DELETE_AND_SEND)
    await edit_dialog_message(manager=manager, text="Поиск...")

    async with TaskiqContext(
            task=get_inn, manager=manager,
            error_log_message="Ошибка поиска ИНН",
            error_user_message="Произошла ошибка поиска ИНН. Задача отменена.",
            timeout_message="Тайм-аут запроса. Задача отменена.",
            make_temp_folder=False
    ) as context:
        inn: str | None = await context.wait_result(timeout=120, data=data)
        if inn is not None:
            await message.answer(f"ИНН - <code>{inn}</code>")
        else:
            await message.answer("Не найдено.")

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


async def error_handler(message: types.Message, _, manager: DialogManager, __):
    await message.delete()
    manager.show_mode = ShowMode.NO_UPDATE


inn_dialog = Dialog(
    Window(
        JinjaTemplate("nwp/inn_parser_message.jinja2"),
        TextInput(
            id="inn_text_data",
            on_success=inn_handler,
            on_error=error_handler,
            type_factory=inn_factory
        ),
        b.CANCEL,
        state=INNParserSG.state
    )
)
