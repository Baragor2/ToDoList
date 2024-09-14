from celery import Celery
from celery.schedules import crontab

from main_service.app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["main_service.app.celery_tasks.tasks"],
)


celery.conf.beat_schedule = {
    'check-tasks-every-minute': {
        'task': 'main_service.app.celery_tasks.tasks.sync_send_message_for_started_tasks',
        'schedule': crontab(minute='*'),
    },
}
