import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.comments.json_parsing import parse_get_comments_json
from app.comments.states import GetComments, CreateComment
from app.config import main_backend_settings
from app.users.auth import generate_tg_hash, get_tg_user_login

router = Router()


@router.message(F.text.lower() == "просмотреть комментарии")
async def get_comments(message: Message, state: FSMContext):
    await message.answer("Введите название мероприятия:")
    await state.set_state(GetComments.waiting_for_task_title)


@router.message(GetComments.waiting_for_task_title)
async def get_task_title(message: Message, state: FSMContext):
    try:
        tg_user_login = await get_tg_user_login(message.from_user.id)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{main_backend_settings.COMMENTS_API_ROOT}comments/{message.text}",
                params=tg_user_login,
            )
        await state.clear()
        comments_message = await parse_get_comments_json(response)
        await message.answer(comments_message)
    except Exception:
        await message.answer("Комментарии отсутствуют")


@router.message(F.text.lower() == "создать комментарий")
async def get_comments(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(CreateComment.waiting_for_task_title)


@router.message(CreateComment.waiting_for_task_title)
async def get_task_title(message: Message, state: FSMContext):
    await state.update_data(task_title=message.text)
    await message.answer("Введите текст комментария:")
    await state.set_state(CreateComment.waiting_for_comment_text)


@router.message(CreateComment.waiting_for_comment_text)
async def get_task_title(message: Message, state: FSMContext):
    await state.update_data(text=message.text)

    tg_user_login = await get_tg_user_login(message.from_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{main_backend_settings.COMMENTS_API_ROOT}comments/",
            json={"comment": await state.get_data(), "tg_user": tg_user_login},
        )

    if response.status_code == 201:
        await message.answer("Комментарий создан")
    else:
        await message.answer(response.json().get("detail"))
    await state.clear()
