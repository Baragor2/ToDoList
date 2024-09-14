from datetime import datetime, UTC
from uuid import uuid4, UUID

from sqlalchemy import delete, and_, update

from app.comments.models import Comments
from app.comments.schemas import SComment, SCommentPatch
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import CommentsException


class CommentsDAO(BaseDAO):
    model = Comments

    @classmethod
    async def create_comment(cls, comment: dict) -> None:
        try:
            await CommentsDAO.add(
                id=uuid4(),
                creation_date=datetime.now(UTC).replace(microsecond=0, tzinfo=None),
                **comment,
            )
        except Exception:
            raise CommentsException

    @classmethod
    async def get_comments(cls, authors_name: str, task_title: str) -> list[SComment]:
        try:
            comments = await CommentsDAO.find_all(
                authors_name=authors_name,
                task_title=task_title,
            )
            return comments
        except Exception:
            raise CommentsException

    @classmethod
    async def delete_comment(cls, comment_id: UUID, task_title: str, authors_name: str) -> None:
        try:
            async with async_session_maker() as session:
                delete_comment_stmt = (
                    delete(Comments)
                    .where(
                        and_(
                            Comments.id == comment_id,
                            Comments.task_title == task_title,
                            Comments.authors_name == authors_name,
                        )
                    )
                )

            await session.execute(delete_comment_stmt)
            await session.commit()
        except Exception:
            raise CommentsException

    @classmethod
    async def update_comment_text(cls, comment: SCommentPatch) -> None:
        try:
            async with async_session_maker() as session:
                update_comment_text_stmt = (
                    update(Comments)
                    .where(
                        and_(
                            Comments.id == comment.id,
                            Comments.task_title == comment.task_title,
                            Comments.authors_name == comment.authors_name,
                        )
                    )
                    .values(text=comment.new_text)
                )

            await session.execute(update_comment_text_stmt)
            await session.commit()
        except Exception:
            raise CommentsException
