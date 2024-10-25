from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput

from idiotDiary_old.apps.not_working_place.utils.inn_selenuim import \
    get_inn_selenium
from ...models.inn import INNSchema, inn_factory
from ...states.not_working_place import INNParserSG
from ...utils.message import edit_dialog_message
from ...views import buttons as b
from ...views.types import JinjaTemplate


async def inn_handler(_, __, manager: DialogManager, data: INNSchema):
    mq: ABCBroker = manager.middleware_data["mq"]
    await edit_dialog_message(manager=manager, text="Поиск...")

    try:
        result_inn = await get_inn_selenium(data=data)
        if result_inn is not None:
            message_text = f"ИНН - <code>{result_inn}</code>"
        else:
            message_text = "Не найдено."

    except SeleniumTimeout:
        message_text = (
            "Запрос не может выполниться по независящим от бота причинам. "
            "Возможно, причина в сайте налоговой. Задача отменена."
        )

    await edit_dialog_message(manager=manager, text=message_text)

    manager.show_mode = ShowMode.SEND


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
