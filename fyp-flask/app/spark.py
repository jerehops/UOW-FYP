import os, sys
from celery import Celery
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

spark = Blueprint('spark', __name__)
simple_app = Celery('simple_worker', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@spark.route('/simple_start_task')
def call_method():
    spark.logger.info("Invoking Method ")
    #                        queue name in task folder.function name
    r = simple_app.send_task('tasks.longtime_add', kwargs={'x': 1, 'y': 2})
    spark.logger.info(r.backend)
    return r.id


@spark.route('/simple_task_status/<task_id>')
def get_status(task_id):
    status = simple_app.AsyncResult(task_id, app=simple_app)
    print("Invoking Method ")
    return "Status of the Task " + str(status.state)


@spark.route('/simple_task_result/<task_id>')
def task_result(task_id):
    result = simple_app.AsyncResult(task_id).result
    return "Result of the Task " + str(result)