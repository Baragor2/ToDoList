import datetime
from email.message import EmailMessage

from pydantic import EmailStr

from main_service.app.config import settings


def create_task_started_template(
    task: dict, email_to: EmailStr
) -> EmailMessage:
    email = EmailMessage()

    email["Subject"] = "Задача началась"
    email["From"] = settings.SMTP_USER
    email["To"] = email_to

    email.set_content(
        f"""
            <h1>Ваша запланированная задача началась</h1>
            Вы запланировали задачу '{task.get("title")}' на {task.get("start_date")}
        """,
        subtype="html",
    )
    return email
