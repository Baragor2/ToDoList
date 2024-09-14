import httpx
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.app.config import main_backend_settings
from bot.app.tasks.json_parsing import parse_get_tasks_json
from bot.app.tasks.states import CreateTask
from bot.app.tasks.utils import check_time_form
from bot.app.users.auth import generate_tg_hash, get_tg_user_login

router = Router()


@router.message(F.text.lower() == "просмотреть задачи")
async def get_tasks(message: Message):
    try:
        tg_user_login = await get_tg_user_login(message.from_user.id)

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{main_backend_settings.COMMENTS_API_ROOT}tasks/",
                params=tg_user_login,
            )
        tasks_message = await parse_get_tasks_json(response)
        await message.answer(tasks_message)
    except Exception:
        await message.answer("Неизвестная ошибка")


@router.message(F.text.lower() == "создать задачу")
async def create_task(message: Message, state: FSMContext):
    await message.answer("Введите название задачи:")
    await state.set_state(CreateTask.waiting_for_title)


@router.message(CreateTask.waiting_for_title)
async def get_task_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи:")
    await state.set_state(CreateTask.waiting_for_description)


@router.message(CreateTask.waiting_for_description)
async def get_task_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите дату начала задачи в формате: 2024-09-10 19:19")
    await state.set_state(CreateTask.waiting_for_start_date)


@router.message(CreateTask.waiting_for_start_date)
async def get_task_start_date(message: Message, state: FSMContext):
    task_start_datetime = await check_time_form(message.text)
    if not task_start_datetime:
        await message.answer("Время введено в неверном формате")
    else:
        await state.update_data(start_date=task_start_datetime.strftime("%Y-%m-%dT%H:%M"))
        await message.answer("Введите дату конца задачи в формате: 2024-09-11 20:00")
        await state.set_state(CreateTask.waiting_for_end_date)


@router.message(CreateTask.waiting_for_end_date)
async def get_task_end_date(message: Message, state: FSMContext):
    task_end_datetime = await check_time_form(message.text)
    if not task_end_datetime:
        await message.answer("Время введено в неверном формате")
    else:
        await state.update_data(end_date=task_end_datetime.strftime("%Y-%m-%dT%H:%M"))
        await message.answer("Введите категорию задачи:")
        await state.set_state(CreateTask.waiting_for_category)


@router.message(CreateTask.waiting_for_category)
async def get_task_category(message: Message, state: FSMContext):
    await state.update_data(category_title=message.text)

    tg_user_login = await get_tg_user_login(message.from_user.id)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{main_backend_settings.COMMENTS_API_ROOT}tasks/",
            json={"task": await state.get_data(), "tg_user": tg_user_login},
        )

    if response.status_code == 201:
        await message.answer("Задача создана")
    else:
        await message.answer(response.json().get("detail"))
    await state.clear()
