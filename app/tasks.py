import pytz
from my_celery import app, logger
import datetime

logger.info("Tasks file loaded.")


@app.task(name='main_task')
def main_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day-1, hour=0, minute=0, second=0, tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
    # print(date)
    # main()  # Запускаем вашу основную задачу


@app.task(name='every_3_hours_task')
def every_3_hours_task():
    date = datetime.datetime.now()
    main_date = datetime.datetime(
        year=date.year, month=date.month, day=date.day, hour=0, minute=0, second=0,
        tzinfo=pytz.timezone('Europe/Moscow')
    )
    logger.info(f"Start algorithm for date: {main_date}")
