from aiogram.fsm.state import StatesGroup, State


class TripSG(StatesGroup):
    trip_list = State()
    trip = State()
