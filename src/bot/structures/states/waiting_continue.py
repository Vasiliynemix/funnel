from aiogram.fsm.state import StatesGroup, State


class AnnounceState(StatesGroup):
    message = State()
