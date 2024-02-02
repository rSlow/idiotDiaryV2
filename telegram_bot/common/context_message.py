from typing import Optional

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove, ForceReply

TypeKeyboard = InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove | ForceReply | None


class ContextMessageManager:
    def __init__(self, bot: Bot,
                 state: FSMContext,
                 message_text: str,
                 keyboard: Optional[TypeKeyboard] = None):
        self.bot = bot
        self.message: Message | None = None
        self.state = state
        self.message_text = message_text
        self.keyboard = keyboard

    async def __aenter__(self):
        chat_id = self.state.key.chat_id
        self.message = await self.bot.send_message(
            text=self.message_text,
            chat_id=chat_id,
            reply_markup=self.keyboard
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.message is not None:
            await self.message.delete()
