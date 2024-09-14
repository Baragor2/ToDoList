from fastapi import HTTPException, status


class ToDoListException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectUsernameOrPasswordException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверное имя пользователя или пароль"


class UserIsNotActiveException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Пользователь не активен"


class UserAlreadyExistsException(ToDoListException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Пользователь уже существует"


class TokenExpiredException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен истёк"


class TokenAbsentException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Токен отсутствует"


class IncorrectTokenFormatException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный формат токена"


class UserIsNotPresentException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED


class NoSuchCategoryException(ToDoListException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой категории не существует"


class CategoryAlreadyExistsException(ToDoListException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Категория уже существует"


class WrongTimeException(ToDoListException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Время должно быть в формате: 2024-08-28T17:06"


class TaskAlreadyExistsException(ToDoListException):
    status_code = status.HTTP_409_CONFLICT
    detail = "Задача уже существует"


class NoSuchTaskException(ToDoListException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Такой задачи не существует"


class NotEnoughRightsException(ToDoListException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Недостаточно прав"


class ThereAreTasksWithCategoryException(ToDoListException):
    status_code = status.HTTP_409_CONFLICT
    detail = "С этой категорией существуют задачи"


class IncorrectTgHashException(ToDoListException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный хэш"
