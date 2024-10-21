__all__ = [
    "RestaurantSG",
]

from aiogram.fsm.state import StatesGroup, State


class RestaurantSG(StatesGroup):
    cuisines = State()
    type_ = State()
    restaurants = State()
    restaurant = State()
