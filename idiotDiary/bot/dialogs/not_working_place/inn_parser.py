from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput
from taskiq import AsyncTaskiqTask, TaskiqResultTimeoutError, TaskiqResult

from idiotDiary.bot.models.inn import INNSchema, inn_factory
from idiotDiary.bot.states.not_working_place import INNParserSG
from idiotDiary.bot.utils.exceptions import TaskiqTaskError
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.views import buttons as b
from idiotDiary.bot.views.types import JinjaTemplate
from idiotDiary.mq.tasks.inn import get_inn


async def inn_handler(
        message: types.Message, __, manager: DialogManager, data: INNSchema
):
    await edit_dialog_message(manager=manager, text="Поиск...")

    try:
        task: AsyncTaskiqTask = await get_inn.kiq(data)
        inn: TaskiqResult = await task.wait_result(timeout=120)
        if error := inn.error:
            await message.answer(
                "Произошла ошибка поиска ИНН. Задача отменена."
            )
            raise TaskiqTaskError(
                message="Ошибка поиска ИНН:", error=error
            )

        if result_inn := inn.return_value:
            await message.answer(f"ИНН - <code>{result_inn}</code>")
        else:
            await message.answer("Не найдено.")

    except TaskiqResultTimeoutError:
        await message.answer("Тайм-аут запроса. Задача отменена.")

    finally:
        manager.show_mode = ShowMode.DELETE_AND_SEND
        await manager.done()


async def error_handler(message: types.Message, _, manager: DialogManager, __):
    await message.delete()
    manager.show_mode = ShowMode.NO_UPDATE


inn_dialog = Dialog(
    Window(
        JinjaTemplate(template_name="inn_parser_message.jinja2"),
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
