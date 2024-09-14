from datetime import datetime

from pydantic import BaseModel


class STask(BaseModel):
    title: str
    authors_name: str
    description: str
    start_date: datetime
    end_date: datetime
    category_title: str


class SCreateTask(BaseModel):
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    category_title: str
