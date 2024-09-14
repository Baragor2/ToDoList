from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SComment(BaseModel):
    id: UUID
    authors_name: str
    task_title: str
    text: str
    creation_date: datetime


class SCommentPatch(BaseModel):
    id: UUID
    authors_name: str
    task_title: str
    new_text: str
