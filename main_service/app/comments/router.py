from typing import Any

import httpx
from fastapi import APIRouter, status, Depends, Request
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.comments.schemas import SCommentCreate, SCommentDelete, SCommentPatch
from app.config import comments_settings
from app.tasks.dao import TasksDAO
from app.users.auth import get_tg_user
from app.users.dependencies import get_current_user
from app.users.schemas import SProfile, STgLogin

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)

limiter = Limiter(key_func=get_remote_address)


@router.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("15/minute")
async def post_comment(
        comment: SCommentCreate,
        request: Request,
        tg_user: STgLogin = None,
) -> tuple[int, Any]:
    if tg_user:
        current_user = await get_tg_user(tg_user.tg_id, tg_user.tg_hash)
    else:
        current_user = await get_current_user(request)

    await TasksDAO.check_task_not_exists(comment.task_title, current_user.username)

    new_comment = {
        "authors_name": current_user.username,
        "task_title": comment.task_title,
        "text": comment.text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{comments_settings.COMMENTS_API_ROOT}comments/", json=new_comment)
        return response.status_code, response.json()


@router.get("/{task_title}")
@limiter.limit("15/minute")
async def get_my_comments_for_task(
        task_title: str,
        request: Request,
        tg_id: str = None,
        tg_hash: str = None,
) -> tuple[int, Any]:
    if tg_id and tg_hash:
        current_user = await get_tg_user(tg_id, tg_hash)
    else:
        current_user = await get_current_user(request)

    await TasksDAO.check_task_not_exists(task_title, current_user.username)

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{comments_settings.COMMENTS_API_ROOT}comments/{task_title}",
            params={"authors_name": current_user.username}
        )

    return response.status_code, response.json()


@router.delete("/")
@limiter.limit("15/minute")
async def delete_comment(
        request: Request, # noqa
        comment: SCommentDelete,
        current_user: SProfile = Depends(get_current_user),
) -> tuple[int, Any]:
    await TasksDAO.check_task_not_exists(comment.task_title, current_user.username)

    comment_data_for_delete = {
        "comment_id": str(comment.id),
        "task_title": comment.task_title,
        "authors_name": current_user.username,
    }

    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{comments_settings.COMMENTS_API_ROOT}comments/",
            params=comment_data_for_delete,
        )

    return response.status_code, response.json()


@router.patch("/")
@limiter.limit("15/minute")
async def change_comment_text_comment(
        request: Request, # noqa
        comment: SCommentPatch,
        current_user: SProfile = Depends(get_current_user),
) -> tuple[int, Any]:
    await TasksDAO.check_task_not_exists(comment.task_title, current_user.username)

    comment_data_for_patch = {
        "comment_id": str(comment.id),
        "task_title": comment.task_title,
        "authors_name": current_user.username,
        "new_text": comment.new_text,
    }

    async with httpx.AsyncClient() as client:
        response = await client.patch(
            f"{comments_settings.COMMENTS_API_ROOT}comments/",
            json=comment_data_for_patch,
        )

    return response.status_code, response.json()
