from aiogram.fsm.state import StatesGroup, State


class GetComments(StatesGroup):
    waiting_for_task_title = State()


class CreateComment(StatesGroup):
    waiting_for_task_title = State()
    waiting_for_comment_text = State()
