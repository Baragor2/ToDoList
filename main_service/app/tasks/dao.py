from sqlalchemy import delete, and_, update

from main_service.app.database import async_session_maker
from main_service.app.exceptions import TaskAlreadyExistsException, NoSuchTaskException
from main_service.app.tasks.models import Tasks
from main_service.app.dao.base import BaseDAO
from main_service.app.tasks.schemas import STask, SCreateTask


class TasksDAO(BaseDAO):
    model = Tasks

    @classmethod
    async def check_task_exists(cls, task_title: str, authors_name: str) -> None:
        task = await cls.find_one_or_none(title=task_title, authors_name=authors_name)
        if task:
            raise TaskAlreadyExistsException

    @classmethod
    async def check_task_not_exists(cls, task_title: str, authors_name: str):
        task = await TasksDAO.find_one_or_none(title=task_title, authors_name=authors_name)
        if not task:
            raise NoSuchTaskException

    @classmethod
    async def delete_task(cls, task_title: str, authors_name: str) -> None:
        async with async_session_maker() as session:
            delete_task_stmt = (
                delete(Tasks)
                .where(
                    and_(
                        Tasks.title == task_title,
                        Tasks.authors_name == authors_name,
                    )
                )
            )

            await session.execute(delete_task_stmt)
            await session.commit()

    @classmethod
    async def update_task(
            cls,
            task_title: str,
            authors_name: str,
            new_task: SCreateTask,
    ) -> None:
        async with async_session_maker() as session:
            update_task_stmt = (
                update(Tasks)
                .where(
                    and_(
                        Tasks.title == task_title,
                        Tasks.authors_name == authors_name,
                    )
                )
                .values(**dict(new_task))
            )

            await session.execute(update_task_stmt)
            await session.commit()
