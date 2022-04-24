from cgi import test
import os

from sqlalchemy import null
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.task()
def spark_job_task(self):
    return null