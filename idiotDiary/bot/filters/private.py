from aiogram import Router, F
from aiogram.enums import ChatType


def set_chat_private_filter(router: Router):
    router.message.filter(F.chat.type == ChatType.PRIVATE)
    router.callback_query.filter(F.message.chat.type == ChatType.PRIVATE)


def set_chat_group_filter(router: Router):
    router.message.filter(F.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
    router.callback_query.filter(F.message.chat.type.in_([ChatType.GROUP, ChatType.SUPERGROUP]))
