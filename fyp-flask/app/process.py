import os, json

from sqlalchemy import false, true
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Blueprint, url_for, render_template, request, jsonify, redirect, session
from flask_login import login_required, current_user
from .models import History
from . import db
logger = get_task_logger(__name__)
process = Blueprint('process', __name__)
celery = Celery('task', broker='redis://redis:6379/0')
    
@process.route('/sparktask', methods=['GET','POST'])
@login_required
def sparktask():
    uid = str(current_user.id)
    if current_user.is_authenticated:
        data = json.loads(request.data)
        results = spark_job_task.apply_async(args=[uid, json.dumps(data)])
        session['task_id'] = str(results)
        return url_for('process.loading')
    else:
        return jsonify({'Error': 'User is not authenticated'}), 400

@process.route('/loading')
@login_required
def loading():
    return render_template('loading.html')

@process.route('/updateData', methods=['POST'])
def update_data():
    if not request.form or 'image' not in request.form:
        return "error", 400
    image_data = request.form['image']
    user_id = request.form['user_id']
    timestamp = request.form['timestamp']
    task_id = request.form['task_id']
    newImage = History(task_id=task_id, imagestring=image_data, user_id=user_id, datetime=timestamp)
    db.session.add(newImage)
    db.session.commit()
    return "success", 201

@process.route('/refreshData')
@login_required
def refresh_data():
    task_completed = History.query.filter_by(user_id=str(current_user.id), task_id=session['task_id']).first()
    if task_completed:
        return jsonify(output="completed", url=url_for('process.results'))
    else:
        return jsonify(output="processing")

@process.route('/results', methods=['GET','POST'])
@login_required
def results():
    image_data = History.query.filter_by(user_id=str(current_user.id), task_id=session['task_id']).first()
    session['task_id']= ""
    return render_template('results.html', image_data=image_data.imagestring)

@celery.task(bind=True)
def spark_job_task(self, uid, data):
    task_id = self.request.id
    master_path = 'local[*]'
    data=json.dumps(data)
    #master_path = 'spark://spark-master:7077'
    spark_code_path = 'scripts/prod.py'
    os.system("spark-submit --master %s %s %s %s %s" % 
        (master_path, spark_code_path, task_id, uid, data))
    return self.request.id