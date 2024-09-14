import logging
import smtplib
from datetime import datetime, UTC, timedelta

from asgiref.sync import async_to_sync

from app.config import settings
from app.tasks.dao import TasksDAO
from app.tasks.schemas import STask
from app.users.dao import UsersDAO
from app.users.schemas import SUser
from app.celery_tasks.email_templates import create_task_started_template
from app.celery_tasks.main_celery import celery


@celery.task
def sync_send_message_for_started_tasks():
    async_to_sync(send_message_for_started_tasks)()


async def send_message_for_started_tasks() -> None:
    tasks: list[STask] = await TasksDAO.find_all()
    for task in tasks:
        if task.start_date <= datetime.now() <= task.start_date + timedelta(minutes=1):
            user: SUser = await UsersDAO.find_one_or_none(username=task.authors_name)

            msg_content = create_task_started_template(dict(task), user.email)

            with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.login(settings.SMTP_USER, settings.SMTP_PASS)
                server.send_message(msg_content)

