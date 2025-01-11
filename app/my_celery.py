from celery import Celery
from celery.schedules import crontab
import pytz
import datetime
from app.settings import logger
from app.main import main


logger.info("Starting Celery")

app = Celery('app', broker='redis://redis:6379/0')
app.conf.timezone = 'Europe/Moscow'


@app.task(name='main_task')
def main_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day-1, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
    main(main_date)


@app.task(name='every_3_hours_task')
def every_3_hours_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0,
        tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
    main(main_date)


app.conf.beat_schedule = {
    'run-main-task-every-day-at-1am': {
        'task': 'main_task',
        'schedule': crontab(hour=0, minute=30),
    },
    'run-main-task-every-3-hours-1': {
        'task': 'every_3_hours_task',
        'schedule': crontab(hour='*/3'),
    },
}
