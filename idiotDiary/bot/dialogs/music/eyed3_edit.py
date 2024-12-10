import uuid
from operator import itemgetter
from pathlib import Path

import aiofiles.tempfile as atf
from aiogram import Bot
from aiogram import types
from aiogram.enums import ContentType, ChatAction
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd import Select, Row, Group
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.text import Format
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from eyed3.id3 import Tag
from taskiq import TaskiqResult

from idiotDiary.bot.schemas.music import EyeD3ActionsEnum, EyeD3MessagesEnum
from idiotDiary.bot.services.music import initialize_audio_file, set_thumbnail
from idiotDiary.bot.states.music import Eyed3EditSG
from idiotDiary.bot.utils.message import edit_dialog_message
from idiotDiary.bot.utils.taskiq_context import TaskiqContext
from idiotDiary.bot.utils.type_factory import regexp_factory, HTTPS_REGEXP
from idiotDiary.bot.views import buttons as b
from idiotDiary.bot.views.alert import BotAlert
from idiotDiary.bot.views.types import JinjaTemplate
from idiotDiary.core.config import Paths
from idiotDiary.mq.tasks.music import download_youtube_audio, process_thumbnail


# ----- INITIALIZE FROM FILE ----- #
async def audio_handler(message: types.Message, _, manager: DialogManager):
    await message.delete()
    await initialize_audio_file(message, manager)


# ----- INITIALIZE FROM URL ----- #
async def url_handler(message: types.Message, _, manager: DialogManager, url: str):
    await message.delete()
    await edit_dialog_message(manager=manager, text="Скачиваю...")

    async with TaskiqContext(
            task=download_youtube_audio, manager=manager,
            error_log_message="Ошибка скачивания аудио:",
            error_user_message="Произошла ошибка скачивания файла. Загрузка отменена.",
            timeout_message="Превышено время скачивания видео.",
    ) as context:
        await message.bot.send_chat_action(
            chat_id=message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        audio_file_path: Path = await context.wait_result(
            timeout=120, temp_path=context.temp_folder, url=url
        )
        await edit_dialog_message(manager=manager, text="Отправляю файл...")
        audio_file = types.FSInputFile(path=audio_file_path)
        audio_message = await message.answer_document(document=audio_file)

    await initialize_audio_file(message=audio_message, manager=manager)


async def invalid_url(message: types.Message, *_):
    await message.answer("Неверный формат ссылки.")


eyed3_start_window = Window(
    Const("Ожидаю файл или ссылку на YouTube..."),
    b.CANCEL,
    MessageInput(
        func=audio_handler,
        content_types=[ContentType.AUDIO]
    ),
    TextInput(
        id="url",
        on_success=url_handler,
        on_error=invalid_url,
        type_factory=regexp_factory(HTTPS_REGEXP)
    ),
    state=Eyed3EditSG.get_file
)


async def edit_window_getter(dialog_manager: DialogManager, **__):
    buttons = [(action.value, action.name) for action in EyeD3ActionsEnum]
    data = {"buttons": buttons}
    data.update(dialog_manager.dialog_data)
    return data


async def category_button_click(_, __, manager: DialogManager, category: str):
    manager.dialog_data["active_category"] = category
    await manager.next()


# ----- SAVE ----- #
@inject
async def eyed3_export(
        callback: types.CallbackQuery, _, manager: DialogManager,
        bot: FromDishka[Bot], paths: FromDishka[Paths], alert: FromDishka[BotAlert]
):
    await callback.message.edit_text("Обработка...")

    dialog_data = manager.dialog_data

    file_id = dialog_data["file_id"]
    download_filename = f"{uuid.uuid4().hex}.mp3"
    filename = dialog_data.get("filename")

    async with atf.TemporaryDirectory(dir=paths.temp_folder_path) as temp_dir:
        temp_path = Path(temp_dir)
        download_file_path = temp_path / download_filename
        await bot.download(file=file_id, destination=download_file_path)

        eyed3_tag = Tag()
        eyed3_tag.album = dialog_data.get("album")
        eyed3_tag.title = dialog_data.get("title")
        eyed3_tag.artist = dialog_data.get("artist")

        thumbnail_id = dialog_data.get("thumbnail")
        if thumbnail_id is not None:
            thumbnail_path = temp_path / f"{uuid.uuid4().hex}.jpeg"
            await bot.download(file=thumbnail_id, destination=thumbnail_path)
            task = await process_thumbnail.kiq(image_path=thumbnail_path)
            res: TaskiqResult = await task.wait_result(timeout=15)
            if res.is_err:
                await alert(f"Ошибка генерации обложки: {repr(res.error)}")
            else:
                manager.dialog_data["thumbnail_path"] = res.return_value
                await set_thumbnail(eyed3_tag, res.return_value)

        eyed3_tag.save(download_file_path.as_posix())

        if eyed3_tag.artist and eyed3_tag.title:
            filename = f"{eyed3_tag.artist} - {eyed3_tag.title}.mp3"

        audio_file = types.FSInputFile(
            path=download_file_path,
            filename=filename or download_filename
        )
        thumbnail_path = manager.dialog_data.get("thumbnail_path")
        if thumbnail_path:
            aiogram_thumbnail = types.FSInputFile(path=thumbnail_path)
        else:
            aiogram_thumbnail = None

        await callback.bot.send_chat_action(
            chat_id=callback.message.chat.id, action=ChatAction.UPLOAD_DOCUMENT
        )
        await callback.message.answer_document(document=audio_file, thumbnail=aiogram_thumbnail)

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


eyed3_main_window = Window(
    JinjaTemplate("music/eyed3_data.jinja2"),
    Group(
        Select(
            id="buttons",
            text=Format("{item[0]}"),
            item_id_getter=itemgetter(1),
            items="buttons",
            on_click=category_button_click
        ),
        width=2
    ),
    Button(
        Const("Сохранить 💾"),
        id="save",
        on_click=eyed3_export  # noqa
    ),
    b.CANCEL,
    getter=edit_window_getter,
    state=Eyed3EditSG.main
)


async def edit_category_getter(dialog_manager: DialogManager, **__):
    category = dialog_manager.dialog_data["active_category"]
    category_text = EyeD3MessagesEnum[category].value
    return {"category_text": category_text}


# ----- EDITOR TEXT ----- #
async def text_handler(
        message: types.Message, _, manager: DialogManager, value: str
):
    category = manager.dialog_data["active_category"]
    if category not in [
        EyeD3ActionsEnum.title.name,
        EyeD3ActionsEnum.artist.name,
        EyeD3ActionsEnum.album.name,
    ]:
        raise RuntimeError("unexpected category to edit")

    manager.show_mode = ShowMode.EDIT
    manager.dialog_data.update({category: value})
    await message.delete()
    await manager.back()


# ----- EDITOR PHOTO ----- #

async def photo_handler(message: types.Message, _, manager: DialogManager):
    category = manager.dialog_data["active_category"]
    if category not in [EyeD3ActionsEnum.thumbnail.name]:
        raise RuntimeError("unexpected category to edit")

    if photos := message.photo:
        value = photos[-1].file_id
    elif document := message.document:
        value = document.file_id
    else:
        raise TypeError("can't read file_id from message file")

    manager.show_mode = ShowMode.EDIT
    manager.dialog_data.update({category: value})
    await message.delete()
    await manager.back()


# ----- CLEANER ----- #

async def clear_category(_, __, manager: DialogManager):
    category = manager.dialog_data["active_category"]
    manager.dialog_data.update({category: None})
    await manager.back()


eyed3_edit_window = Window(
    Format("{category_text}"),
    Row(
        Button(
            id="clear_category",
            text=Const("Очистить 🗑"),
            on_click=clear_category
        ),
        b.BACK
    ),
    TextInput(
        id="text_value",
        on_success=text_handler,
    ),
    MessageInput(
        func=photo_handler,
        content_types=[
            ContentType.PHOTO,
            ContentType.DOCUMENT
        ]
    ),
    getter=edit_category_getter,
    state=Eyed3EditSG.edit
)

eyed3_edit_dialog = Dialog(
    eyed3_start_window,
    eyed3_main_window,
    eyed3_edit_window
)
