from aiogram import Router, F
from aiogram.enums import ChatType


def set_chat_private_filter(router: Router):
    router.message.filter(F.chat.type == ChatType.PRIVATE)
