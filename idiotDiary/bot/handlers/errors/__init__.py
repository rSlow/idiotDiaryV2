from aiogram import Dispatcher

from . import dialogs, base


def setup(dp: Dispatcher):
    dialogs.setup(dp)
    base.setup(dp)
