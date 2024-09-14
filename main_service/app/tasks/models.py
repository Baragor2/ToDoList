from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from main_service.app.database import Base
from main_service.app.categories.models import Categories # noqa


class Tasks(Base):
    __tablename__ = 'tasks'

    title: Mapped[str] = mapped_column(primary_key=True)
    authors_name: Mapped[str] = mapped_column(ForeignKey('users.username'), primary_key=True)
    description: Mapped[str] = mapped_column(nullable=True)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    end_date: Mapped[datetime] = mapped_column(nullable=False)
    category_title: Mapped[str] = mapped_column(ForeignKey('categories.title'), nullable=False)

    user = relationship("Users", back_populates="task")
    category = relationship("Categories", back_populates="task")

    def __str__(self):
        return f"Задача {self.title}"
