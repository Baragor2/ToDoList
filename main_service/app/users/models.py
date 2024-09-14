from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(primary_key=True)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="User")
    tg_id: Mapped[str] = mapped_column(unique=True, nullable=True)
    tg_hash: Mapped[str] = mapped_column(unique=True, nullable=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    task = relationship("Tasks", back_populates="user")

    def __str__(self):
        return f"Пользователь {self.username}"
