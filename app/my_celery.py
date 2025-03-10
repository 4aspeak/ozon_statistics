import datetime

import pytz
from celery import Celery
from celery.schedules import crontab

from app.main import main
from app.settings import logger

logger.info("Starting Celery")

app = Celery('app', broker='redis://redis:6379/0')

# Настройка параметров Celery
app.conf.update(
    timezone='Europe/Moscow',
    broker_connection_retry_on_startup=True,
)


@app.task(name='at_last_day_task')
def at_last_day_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day-1, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
    main(main_date)


@app.task(name='at_this_day_task')
def at_this_day_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0,
        tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
    main(main_date)


app.conf.beat_schedule = {
    'run-main-task-last-day-at-1am': {
        'task': 'at_last_day_task',
        'schedule': crontab(hour=0, minute=30),
    },
    'run-main-task-last-day-at-3am': {
        'task': 'at_last_day_task',
        'schedule': crontab(hour=3, minute=30),
    },
    'run-main-task-every-day-at-3am': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=3, minute=0),
    },
    'run-main-task-every-day-at-6am': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=6, minute=0),
    },
    'run-main-task-every-day-at-9am': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=9, minute=0),
    },
    'run-main-task-every-day-at-12pm': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=12, minute=0),
    },
    'run-main-task-every-day-at-15pm': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=15, minute=0),
    },
    'run-main-task-every-day-at-18pm': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=18, minute=0),
    },
    'run-main-task-every-day-at-21pm': {
        'task': 'at_this_day_task',
        'schedule': crontab(hour=21, minute=0),
    },
}
