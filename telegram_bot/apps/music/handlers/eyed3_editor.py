import uuid
from operator import itemgetter

import eyed3
from aiogram import types, Bot
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput, TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import Select, Button, Row, Group
from aiogram_dialog.widgets.text import Const, Format
from eyed3.id3 import Tag

from common.dialogs.types import JinjaTemplate
from common.filters import regexp_factory
from common.buttons import CANCEL_BUTTON, BACK_BUTTON
from common.utils.decorators import to_async_thread
from common.utils.functions import edit_dialog_message
from .. import settings
from ..states import EyeD3FSM
from ..enums import EyeD3ActionsEnum, EyeD3MessagesEnum
from ..utils.audio import download_audio
from ..utils.image import process_image, get_aiogram_thumbnail
from ..utils.temp_dowlnoader import TempFileDownloader


async def initialize_audio_file(message: types.Message,
                                manager: DialogManager):
    bot: Bot = manager.middleware_data["bot"]

    audio = message.audio
    file_id = audio.file_id
    filename = audio.file_name or uuid.uuid4().hex + settings.AUDIO_FILE_EXT
    file_path = settings.TEMP_DIR / filename

    await edit_dialog_message(
        manager=manager,
        text="Обработка..."
    )
    async with TempFileDownloader(file_path=file_path,
                                  bot=bot,
                                  file_id=file_id):
        eyed3_audio = await to_async_thread(eyed3.load)(file_path)
        if eyed3_audio is None:
            await message.answer(
                text="Невозможно распознать файл. Попробуйте загрузить другой файл."
            )
            return await manager.done()

        eyed3_tag: Tag = eyed3_audio.tag if eyed3_audio.tag is not None else Tag()

        album = eyed3_tag.album
        title = audio.title
        artist = audio.performer
        thumbnail = audio.thumbnail.file_id if audio.thumbnail else None
        manager.dialog_data.update({
            "filename": filename,
            "file_id": file_id,
            "album": album,
            "title": title,
            "artist": artist,
            "thumbnail": thumbnail
        })

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.next()


# ----- INITIALIZE FROM FILE ----- #
async def audio_handler(message: types.Message,
                        _: MessageInput,
                        manager: DialogManager):
    await message.delete()
    await initialize_audio_file(
        message=message,
        manager=manager
    )


# ----- INITIALIZE FROM URL ----- #
async def url_handler(message: types.Message,
                      __: ManagedTextInput,
                      manager: DialogManager,
                      url: str):
    await message.delete()
    await edit_dialog_message(
        manager=manager,
        text="Скачиваю..."
    )
    result = await download_audio(
        url=url,
        root_temp_path=settings.TEMP_DIR
    )
    audio_file = types.BufferedInputFile(
        file=result.data,
        filename=result.filename
    )
    audio = await message.answer_document(document=audio_file)
    await initialize_audio_file(
        message=audio,
        manager=manager
    )


async def invalid_url(message: types.Message, *_):
    await message.answer("Неверный формат ссылки.")


eyed3_start_window = Window(
    Const("Ожидаю файл или ссылку на YouTube..."),
    CANCEL_BUTTON,
    MessageInput(
        func=audio_handler,
        content_types=[ContentType.AUDIO]
    ),
    TextInput(
        id="url",
        on_success=url_handler,
        on_error=invalid_url,
        type_factory=regexp_factory(settings.HTTPS_REGEXP)
    ),
    state=EyeD3FSM.wait_file
)


async def edit_window_getter(dialog_manager: DialogManager, **__):
    buttons = [(action.value, action.name)
               for action in EyeD3ActionsEnum]
    data = {"buttons": buttons}
    data.update(dialog_manager.dialog_data)
    return data


async def category_button_click(_: types.CallbackQuery,
                                __: Button,
                                manager: DialogManager,
                                category: str):
    manager.dialog_data["active_category"] = category
    await manager.next()


# ----- SAVE ----- #
async def eyed3_export(callback: types.CallbackQuery,
                       __: Button,
                       manager: DialogManager):
    bot: Bot = manager.middleware_data["bot"]
    eyed3_data = manager.dialog_data

    file_id = eyed3_data.get("file_id")
    filename = eyed3_data.get("filename", uuid.uuid4().hex + settings.AUDIO_FILE_EXT)
    file_path = settings.TEMP_DIR / filename

    await callback.message.edit_text("Обработка...")

    async with TempFileDownloader(file_path=file_path,
                                  bot=bot,
                                  file_id=file_id):
        eyed3_tag: Tag = Tag()
        eyed3_tag.album = eyed3_data.get("album")
        eyed3_tag.title = eyed3_data.get("title")
        eyed3_tag.artist = eyed3_data.get("artist")

        thumbnail_id = eyed3_data.get("thumbnail")
        if thumbnail_id is not None:
            # delete all existing
            for image in eyed3_tag.images:
                eyed3_tag.images.remove(image.description)

            image_io = await bot.download(thumbnail_id)
            processed_image_io = await process_image(image_io)
            eyed3_tag.images.set(
                type_=3,
                img_data=await to_async_thread(processed_image_io.read)(),
                mime_type="image/jpeg"
            )

        eyed3_tag.save(file_path.as_posix())

        if eyed3_tag.artist and eyed3_tag.title:
            filename = f"{eyed3_tag.artist} - {eyed3_tag.title}{settings.AUDIO_FILE_EXT}"

        audio_file = types.FSInputFile(
            path=file_path,
            filename=filename
        )
        await callback.message.answer_document(
            document=audio_file,
            thumbnail=await get_aiogram_thumbnail(processed_image_io) if thumbnail_id is not None else None
        )

    manager.show_mode = ShowMode.DELETE_AND_SEND
    await manager.done()


eyed3_main_window = Window(
    JinjaTemplate(
        template_name="eyed3_data.jinja2",
        templates_dir=settings.TEMPLATES_DIR
    ),
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
        on_click=eyed3_export
    ),
    CANCEL_BUTTON,
    getter=edit_window_getter,
    state=EyeD3FSM.main
)


async def edit_category_getter(dialog_manager: DialogManager, **__):
    category = dialog_manager.dialog_data["active_category"]
    category_text = EyeD3MessagesEnum[category].value
    return {"category_text": category_text}


# ----- EDITOR TEXT ----- #
async def text_handler(message: types.Message,
                       _: ManagedTextInput,
                       manager: DialogManager,
                       value: str):
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

async def photo_handler(message: types.Message,
                        _: MessageInput,
                        manager: DialogManager) -> None:
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
async def clear_category(_: types.CallbackQuery,
                         __: Button,
                         manager: DialogManager):
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
        BACK_BUTTON
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
    state=EyeD3FSM.edit
)

music_eyed3_dialog = Dialog(
    eyed3_start_window,
    eyed3_main_window,
    eyed3_edit_window
)
