from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    authors_name: Mapped[str] = mapped_column(nullable=False)
    task_title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    creation_date: Mapped[datetime] = mapped_column(nullable=False)
