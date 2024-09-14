from aiogram.fsm.state import StatesGroup, State


class CreateTask(StatesGroup):
    waiting_for_title = State()
    waiting_for_description = State()
    waiting_for_start_date = State()
    waiting_for_end_date = State()
    waiting_for_category = State()
