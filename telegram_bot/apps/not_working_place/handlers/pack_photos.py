from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from ..FSM.start import Start
from ..FSM.images_zip import ImagesZip
from ..keyboards.main import NotWorkingPlaceKeyboard
from ..keyboards.pack import PackKeyboard, PackFinishKeyboard
from ..utils import photos

pack_photos_router = Router(name="pack_photos")


@pack_photos_router.message(
    F.text == NotWorkingPlaceKeyboard.Buttons.pack,
    Start.main
)
async def wait_photos(message: types.Message, state: FSMContext):
    await state.set_state(ImagesZip.start)

    await photos.init_photos_proxy(state)

    await message.answer(
        text="Жду фотографий. Как отправлены все - нажать 'Запаковать!'",
        reply_markup=PackKeyboard.build()
    )


@pack_photos_router.message(
    F.photo,
    StateFilter(ImagesZip.waiting, ImagesZip.start)
)
async def append_photo(message: types.Message, state: FSMContext):
    await state.set_state(ImagesZip.waiting)

    file_id = message.photo[-1].file_id
    await photos.add_photo_file_id(state, file_id)
    await message.delete()


@pack_photos_router.message(
    F.text == PackKeyboard.Buttons.accept,
    ImagesZip.waiting
)
async def return_zip(message: types.Message, state: FSMContext):
    file_id_list = await photos.get_file_id_list(state)
    await photos.clear_file_id_list(state)

    if not file_id_list:
        await message.answer(
            text="Не было отправлено ни одной фотографии, пробуем еще раз!"
        )
        await wait_photos(message=message, state=state)

    else:
        temp_message = await message.answer(
            text=f"Запаковывается {len(file_id_list)} фотографий..."
        )

        await state.set_state(ImagesZip.finish)
        zip_file = await photos.get_zip_file(file_id_list, bot=message.bot)

        await temp_message.delete()

        temp_message = await message.answer(
            text="Архив отправляется..."
        )
        await message.answer_document(
            document=zip_file,
            reply_markup=PackFinishKeyboard.build()
        )
        await temp_message.delete()


@pack_photos_router.message(
    F.text == PackFinishKeyboard.Buttons.again,
    ImagesZip.finish
)
async def zip_again(message: types.Message, state: FSMContext):
    await wait_photos(message=message, state=state)
