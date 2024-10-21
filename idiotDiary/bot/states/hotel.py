__all__ = [
    "HotelSG",
]

from aiogram.fsm.state import StatesGroup, State


class HotelSG(StatesGroup):
    district = State()
    hotels = State()
    hotel = State()
