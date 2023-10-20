import uuid
from typing import Any

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Bot
from aiogram.types import FSInputFile, ReplyKeyboardRemove
from eyed3.id3 import Tag

from common.jinja import render_template
from common.utils.sync_to_async import set_async
from .. import settings
from ..keyboards.eyed3_main import EyeD3MainKeyboard, EyeD3BackToMainKeyboard
from ..keyboards.main import MusicMainKeyboard
import eyed3

from common.keyboards.base import CancelKeyboard
from ..FSM.main import MusicState, EyeD3State, EyeD3EditState
from ..utils.temp_dowlnoader import TempFileDownloader

music_eyed3_router = Router(name="music_eyed3")


@music_eyed3_router.message(
    F.text == MusicMainKeyboard.Buttons.edit_music,
    MusicState.start
)
async def start_eyed3_editor(message: types.Message, state: FSMContext):
    await state.set_state(EyeD3State.wait_file)
    await message.answer(
        text=f"Ожидаю файл{'или ссылку на YouTube' if False else ''}...",
        reply_markup=CancelKeyboard.build(one_time_keyboard=True)
    )


# ----- INITIALIZE ----- #

@music_eyed3_router.message(
    F.audio.as_("audio"),
    EyeD3State.wait_file
)
async def eyed3_parse_file(message: types.Message, state: FSMContext, audio: types.Audio, bot: Bot):
    file_id = audio.file_id
    filename = f"{uuid.uuid4().hex}.mp3"
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
        title = eyed3_tag.title
        artist = eyed3_tag.artist

        await state.update_data(eyed3_data={
            "file_id": file_id,
            "album": album,
            "title": title,
            "artist": artist,
            "message_id": None
        })
        await message.delete()

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
    F.text,
    StateFilter(EyeD3EditState)
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
    eyed3_data[edited_param] = message.text
    await state.update_data(eyed3_data=eyed3_data)

    chat_id = message.chat.id
    await message.delete()
    await eyed3_main_page(
        state=state,
        bot=bot,
        chat_id=chat_id
    )


# ----- EDITOR LAUNCHERS ----- #

@music_eyed3_router.callback_query(
    F.data == EyeD3MainKeyboard.Buttons.edit_title.callback_data,
    EyeD3State.main
)
async def eyed3_edit_title(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EyeD3EditState.title)
    await callback.message.edit_text(
        text=f"Введите новое название песни...",
        reply_markup=EyeD3BackToMainKeyboard.build()
    )


@music_eyed3_router.callback_query(
    F.data == EyeD3MainKeyboard.Buttons.edit_artist.callback_data,
    EyeD3State.main
)
async def eyed3_edit_artist(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EyeD3EditState.artist)
    await callback.message.edit_text(
        text=f"Введите нового исполнителя...",
        reply_markup=EyeD3BackToMainKeyboard.build()
    )


@music_eyed3_router.callback_query(
    F.data == EyeD3MainKeyboard.Buttons.edit_album.callback_data,
    EyeD3State.main
)
async def eyed3_edit_album(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(EyeD3EditState.album)
    await callback.message.edit_text(
        text=f"Введите новое название альбома...",
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
    filename = f"{uuid.uuid4().hex}.mp3"
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
        eyed3_tag.save(str(file_path))

        audio_file = FSInputFile(
            path=file_path,
            filename=f"{eyed3_tag.artist} - {eyed3_tag.title}.mp3"
        )
        await callback.message.answer_document(
            document=audio_file
        )
