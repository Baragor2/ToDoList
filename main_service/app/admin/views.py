from sqladmin import ModelView

from main_service.app.categories.models import Categories
from main_service.app.tasks.models import Tasks
from main_service.app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.username, Users.role]
    column_details_exclude_list = [
        Users.hashed_password,
        Users.tg_id,
        Users.tg_hash
    ]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class TasksAdmin(ModelView, model=Tasks):
    column_list = [column.name for column in Tasks.__table__.columns] + [
        Tasks.user,
        Tasks.category,
    ]
    name = "Задача"
    name_plural = "Задачи"
    icon = "fa-solid fa-list-check"


class CategoriesAdmin(ModelView, model=Categories):
    column_list = [column.name for column in Tasks.__table__.columns] + [
        Categories.task,
    ]
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-list"
