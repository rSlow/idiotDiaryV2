from aiogram_dialog.widgets.common import ManagedScroll as MScroll


async def normalize_scroll(scroll_data: list, scroll: MScroll) -> None:
    current_page = await scroll.get_page()
    try:
        scroll_data[current_page]
    except IndexError:
        await scroll.set_page(0)
