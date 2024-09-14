from sqlalchemy import update, and_

from main_service.app.database import async_session_maker
from main_service.app.exceptions import UserAlreadyExistsException
from main_service.app.users.models import Users
from main_service.app.dao.base import BaseDAO


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def check_user_exists(cls, username: str) -> None:
        existing_user = await cls.find_one_or_none(username=username)
        if existing_user:
            raise UserAlreadyExistsException

    @classmethod
    async def add_tg_data(cls, username: str, tg_id: str, tg_hash: str) -> None:
        async with async_session_maker() as session:
            update_task_stmt = (
                update(Users)
                .where(Users.username == username)
                .values(
                    tg_id=tg_id,
                    tg_hash=tg_hash,
                )
            )

            await session.execute(update_task_stmt)
            await session.commit()
