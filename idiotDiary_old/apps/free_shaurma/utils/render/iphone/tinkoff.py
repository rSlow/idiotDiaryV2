from PIL import Image, ImageFont

from common.utils.functions import get_now
from .. import settings
from ..image_io_context import ImageIOContext
from ...prepare_data import prepare_tinkoff_sums

x = 1125
y = 2436


def tinkoff_tinkoff_phone_iphone(name: str,
                                 phone_num: str,
                                 start_sum: int | float,
                                 transfer_sum: int | float,
                                 **__):
    str_start_sum, str_transfer_sum, str_end_sum, changing_string = prepare_tinkoff_sums(
        start_sum=start_sum,
        transfer_sum=transfer_sum
    )
    stroked_font = ImageFont.truetype(
        font=settings.font_iphone_thin,
        size=48
    )
    length_line = stroked_font.getlength(str_start_sum)
    length_full = stroked_font.getlength(changing_string)
    start_changing_string = x / 2 - length_full / 2

    with ImageIOContext(settings.template_tinkoff_phone_iphone) as context:
        draw = context.draw


    return context.io
