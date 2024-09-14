from fastapi import APIRouter, status, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.exc import DBAPIError

from app.categories.dao import CategoriesDAO
from app.exceptions import WrongTimeException
from app.tasks.dao import TasksDAO
from app.tasks.schemas import SCreateTask
from app.users.auth import get_tg_user
from app.users.dependencies import get_current_user
from app.users.schemas import SProfile, STgLogin


limiter = Limiter(key_func=get_remote_address)

router = APIRouter(
     prefix="/tasks",
     tags=["Tasks"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def create_task(
        task: SCreateTask,
        request: Request,
        tg_user: STgLogin = None,
) -> None:
    if tg_user:
        current_user = await get_tg_user(tg_user.tg_id, tg_user.tg_hash)
    else:
        current_user = await get_current_user(request)

    await CategoriesDAO.check_category_not_exists(task.category_title)
    await TasksDAO.check_task_exists(task.title, current_user.username)

    try:
        await TasksDAO.add(
             authors_name=current_user.username,
             **dict(task),
        )
    except DBAPIError:
        raise WrongTimeException


@router.get("/")
@limiter.limit("15/minute")
async def get_my_tasks(
        request: Request,
        tg_id: str = None,
        tg_hash: str = None,
) -> list[SCreateTask]:
    if tg_id and tg_hash:
        current_user = await get_tg_user(tg_id, tg_hash)
    else:
        current_user = await get_current_user(request)
    tasks = await TasksDAO.find_all(authors_name=current_user.username)
    return tasks


@router.get("/{category_title}")
@limiter.limit("15/minute")
async def get_my_tasks_by_category(
        request: Request, # noqa
        category_title: str,
        current_user: SProfile = Depends(get_current_user),
) -> list[SCreateTask]:
    await CategoriesDAO.check_category_not_exists(category_title)

    tasks = await TasksDAO.find_all(
        authors_name=current_user.username,
        category_title=category_title,
    )
    return tasks


@router.delete("/{task_title}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("15/minute")
async def delete_task(
        request: Request, # noqa
        task_title: str,
        current_user: SProfile = Depends(get_current_user),
) -> None:
    await TasksDAO.check_task_not_exists(task_title, current_user.username)
    await TasksDAO.delete_task(task_title, current_user.username)


@router.put("/{task_title}")
@limiter.limit("15/minute")
async def put_task(
        request: Request, # noqa
        task_title: str,
        new_task: SCreateTask,
        current_user: SProfile = Depends(get_current_user),
) -> None:
    await CategoriesDAO.check_category_not_exists(new_task.category_title)
    await TasksDAO.check_task_not_exists(task_title, current_user.username)

    try:
        await TasksDAO.update_task(
            task_title=task_title,
            authors_name=current_user.username,
            new_task=new_task,
        )
    except DBAPIError:
        raise WrongTimeException
