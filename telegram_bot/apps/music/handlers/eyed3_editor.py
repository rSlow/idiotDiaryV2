import uuid
from typing import Any

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import FSInputFile, ReplyKeyboardRemove
import eyed3
from eyed3.id3 import Tag

from common.jinja import render_template
from common.utils.sync_to_async import set_async
from .main import music_start
from .. import settings
from ..factory import EyeD3EditCBFactory, EyeD3MessagesEnum, EyeD3ActionsEnum
from ..keyboards.eyed3_main import EyeD3MainKeyboard, EyeD3BackToMainKeyboard
from ..keyboards.main import MusicMainKeyboard

from common.keyboards.base import CancelKeyboard
from ..FSM.main import MusicState, EyeD3State, EyeD3EditState
from ..utils.image import process_image
from ..utils.temp_dowlnoader import TempFileDownloader

music_eyed3_router = Router(name="music_eyed3")


@music_eyed3_router.message(
    F.text == MusicMainKeyboard.Buttons.edit_music,
    MusicState.start
)
async def start_eyed3_editor(message: types.Message, state: FSMContext):
    await state.set_state(EyeD3State.wait_file)
    await message.answer(
        text=f"Ожидаю файл...",
        reply_markup=CancelKeyboard.build(one_time_keyboard=True)
    )


# ----- INITIALIZE ----- #

@music_eyed3_router.message(
    F.audio.as_("audio"),
    EyeD3State.wait_file
)
async def eyed3_parse_file(message: types.Message, state: FSMContext, audio: types.Audio, bot: Bot):
    file_id = audio.file_id
    filename = uuid.uuid4().hex + settings.AUDIO_FILE_EXT
    file_path = settings.TEMP_DIR / filename

    service_message = await message.answer("Обработка...")

    async with TempFileDownloader(file_path=file_path, bot=bot, file_id=file_id, message_to_del=service_message):
        eyed3_audio = await set_async(eyed3.load)(file_path)
        if eyed3_audio is None:
            return await message.answer(
                text="Невозможно распознать файл. Попробуйте загрузить другой файл."
            )

        eyed3_tag: Tag = eyed3_audio.tag if eyed3_audio.tag is not None else Tag()

        album = eyed3_tag.album
        title = audio.title
        artist = audio.performer
        thumbnail = audio.thumbnail.file_id if audio.thumbnail else None
        await state.update_data(eyed3_data={
            "file_id": file_id,
            "album": album,
            "title": title,
            "artist": artist,
            "thumbnail": thumbnail,
            "message_id": None
        })

    await eyed3_main_page(
        chat_id=message.chat.id,
        state=state,
        bot=bot
    )


# ----- MAIN PAGE ----- #

async def eyed3_main_page(
        state: FSMContext,
        bot: Bot,
        chat_id: int,
):
    await state.set_state(EyeD3State.main)
    data = await state.get_data()
    eyed3_data: dict[str, Any] = data.get("eyed3_data", {})

    main_text = render_template(
        template_name="eyed3_data.jinja2",
        data=eyed3_data
    )

    message_id = eyed3_data.get("message_id")
    if message_id is None:
        message = await bot.send_message(
            text=main_text,
            chat_id=chat_id,
            reply_markup=EyeD3MainKeyboard.build()
        )
        eyed3_data.update(message_id=message.message_id)
        await state.update_data(eyed3_data=eyed3_data)

    else:
        await bot.edit_message_text(
            text=main_text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=EyeD3MainKeyboard.build()
        )


# ----- EDITOR ----- #

@music_eyed3_router.message(
    F.text | F.photo,
    StateFilter(EyeD3EditState),
)
async def eyed3_update_param(
        message: types.Message,
        state: FSMContext,
        raw_state: str,
        bot: Bot
):
    data = await state.get_data()
    eyed3_data: dict[str, Any] = data.get("eyed3_data", {})
    edited_param = raw_state.split(":")[-1]

    if edited_param == EyeD3ActionsEnum.thumbnail.value:
        edited_param_value = message.photo[-1].file_id
    else:
        edited_param_value = message.text
    eyed3_data[edited_param] = edited_param_value

    await state.update_data(eyed3_data=eyed3_data)

    chat_id = message.chat.id
    await message.delete()
    await eyed3_main_page(
        state=state,
        bot=bot,
        chat_id=chat_id
    )


# ----- EDITOR LAUNCHER ----- #

@music_eyed3_router.callback_query(
    EyeD3EditCBFactory.filter(),
    EyeD3State.main
)
async def eyed3_edit_param(
        callback: types.CallbackQuery,
        callback_data: EyeD3EditCBFactory,
        state: FSMContext
):
    action_name = callback_data.action.name
    message_text = EyeD3MessagesEnum[action_name].value
    edit_state = getattr(EyeD3EditState, action_name)
    await state.set_state(edit_state)

    await callback.message.edit_text(
        text=message_text,
        reply_markup=EyeD3BackToMainKeyboard.build()
    )


# ----- BACK TO MAIN ----- #

@music_eyed3_router.callback_query(
    F.data == EyeD3BackToMainKeyboard.Buttons.back.callback_data,
    StateFilter(EyeD3EditState)
)
async def eyed3_back_to_main(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await eyed3_main_page(
        bot=bot,
        chat_id=callback.message.chat.id,
        state=state
    )


# ----- SAVE ----- #

@music_eyed3_router.callback_query(
    F.data == EyeD3MainKeyboard.Buttons.export.callback_data,
    EyeD3State.main
)
async def eyed3_export(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    eyed3_data: dict[str, Any] = data.get("eyed3_data", {})

    file_id = eyed3_data.get("file_id")
    chat_id = callback.message.chat.id
    filename = uuid.uuid4().hex + settings.AUDIO_FILE_EXT
    file_path = settings.TEMP_DIR / filename

    await callback.message.delete()
    service_message = await bot.send_message(
        chat_id=chat_id,
        text="Обработка...",
        reply_markup=ReplyKeyboardRemove()
    )

    async with TempFileDownloader(file_path=file_path, bot=bot, file_id=file_id, message_to_del=service_message):
        eyed3_tag: Tag = Tag()
        eyed3_tag.album = eyed3_data.get("album")
        eyed3_tag.title = eyed3_data.get("title")
        eyed3_tag.artist = eyed3_data.get("artist")
        thumbnail = eyed3_data.get("thumbnail")

        if thumbnail is not None:
            # delete all existing
            for image in eyed3_tag.images:
                eyed3_tag.images.remove(image.description)

            image_io = await bot.download(thumbnail)
            processed_image_io = process_image(image_io)
            eyed3_tag.images.set(
                type_=3,
                img_data=processed_image_io.read(),
                mime_type="image/jpeg"
            )

        eyed3_tag.save(str(file_path))

        audio_file = FSInputFile(
            path=file_path,
            filename=f"{eyed3_tag.artist} - {eyed3_tag.title}{settings.AUDIO_FILE_EXT}"
        )
        await callback.message.answer_document(
            document=audio_file
        )
        await music_start(
            message=callback.message,
            state=state
        )
