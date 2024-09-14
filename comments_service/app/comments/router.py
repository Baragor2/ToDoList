import time
from uuid import UUID

from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from comments_service.app.comments.dao import CommentsDAO
from comments_service.app.comments.schemas import SComment, SCommentPatch

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def post_comment(comment: dict) -> dict[str, str]:
    await CommentsDAO.create_comment(comment)
    return {"message": "comment created successfully"}


@router.get("/{task_title}")
@cache(expire=20)
async def get_my_comments_for_task(
        authors_name: str,
        task_title: str,
) -> list[SComment]:
    time.sleep(6)
    comments = await CommentsDAO.get_comments(authors_name, task_title)
    return comments


@router.delete("/")
async def delete_comment(
        comment_id: str,
        task_title: str,
        authors_name: str,
) -> dict[str, str]:
    await CommentsDAO.delete_comment(UUID(comment_id), task_title, authors_name)
    return {"message": "comment deleted successfully"}


@router.patch("/")
async def change_comment_text(comment: dict) -> dict[str, str]:
    await CommentsDAO.update_comment_text(
        SCommentPatch(
            id=UUID(comment.get("comment_id")),
            task_title=comment.get("task_title"),
            authors_name=comment.get("authors_name"),
            new_text=comment.get("new_text"),
        ))
    return {"message": "comment text changed successfully"}
