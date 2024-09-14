from sqlalchemy.orm import Mapped, mapped_column, relationship

from main_service.app.database import Base


class Categories(Base):
    __tablename__ = 'categories'

    title: Mapped[str] = mapped_column(primary_key=True, unique=True)

    task = relationship("Tasks", back_populates="category")

    def __str__(self):
        return f"Категория {self.title}"
