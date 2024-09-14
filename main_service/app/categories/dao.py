from sqlalchemy import delete, update
from sqlalchemy.exc import IntegrityError

from app.categories.models import Categories
from app.categories.schemas import SCategory
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import (NoSuchCategoryException, CategoryAlreadyExistsException,
                                         ThereAreTasksWithCategoryException)


class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    async def check_category_not_exists(cls, category_title: str) -> None:
        category = await cls.find_one_or_none(title=category_title)
        if not category:
            raise NoSuchCategoryException

    @classmethod
    async def check_category_exists(cls, category_title: str) -> None:
        category = await cls.find_one_or_none(title=category_title)
        if category:
            raise CategoryAlreadyExistsException

    @classmethod
    async def delete_category(cls, category_title: str) -> None:
        await CategoriesDAO.check_category_not_exists(category_title)

        try:
            async with async_session_maker() as session:
                delete_task_stmt = (
                    delete(Categories)
                    .where(Categories.title == category_title)
                )

                await session.execute(delete_task_stmt)
                await session.commit()
        except IntegrityError:
            raise ThereAreTasksWithCategoryException

    @classmethod
    async def update_category(cls, category_title: str, category: SCategory) -> None:
        await CategoriesDAO.check_category_not_exists(category_title)

        try:
            async with async_session_maker() as session:
                update_category_stmt = (
                    update(Categories)
                    .where(
                        Categories.title == category_title,
                    )
                    .values(**dict(category))
                )

                await session.execute(update_category_stmt)
                await session.commit()
        except IntegrityError:
            raise ThereAreTasksWithCategoryException
