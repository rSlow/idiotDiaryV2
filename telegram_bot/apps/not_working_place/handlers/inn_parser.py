from aiogram import types
from aiogram_dialog import Dialog, Window, DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput

from common.dialogs.types import JinjaTemplate
from common.buttons import CANCEL_BUTTON
from .. import settings
from ..states import INNParserFSM
from ..factory.inn import inn_factory, INNSchema
from ..utils.inn_selenuim import get_inn_selenium, SeleniumTimeout


async def inn_handler(message: types.Message,
                      _: ManagedTextInput,
                      manager: DialogManager,
                      data: INNSchema):
    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.update({})
    chat_id = message.chat.id
    dialog_message_id: int = manager.current_stack().last_message_id
    await message.bot.edit_message_text(
        chat_id=chat_id,
        message_id=dialog_message_id,
        text="Поиск..."
    )

    try:
        result_inn = await get_inn_selenium(data=data)
        message_text = f"ИНН - <code>{result_inn}</code>" if result_inn is not None else "Не найдено."

    except SeleniumTimeout:
        message_text = ("Запрос не может выполниться по независящим от бота причинам. "
                        "Возможно, причина в сайте налоговой. Задача отменена.")
    finally:
        await message.bot.edit_message_text(
            chat_id=chat_id,
            message_id=dialog_message_id,
            text=message_text
        )

    manager.show_mode = ShowMode.SEND


async def error_handler(message: types.Message,
                        _: ManagedTextInput,
                        manager: DialogManager,
                        __: ValueError):
    await message.delete()
    manager.show_mode = ShowMode.NO_UPDATE


inn_dialog = Dialog(
    Window(
        JinjaTemplate(
            template_name="inn_parser_message.jinja2",
            templates_dir=settings.TEMPLATES_DIR,
        ),
        TextInput(
            id="inn_text_data",
            on_success=inn_handler,
            on_error=error_handler,
            type_factory=inn_factory
        ),
        CANCEL_BUTTON,
        state=INNParserFSM.state
    )
)
