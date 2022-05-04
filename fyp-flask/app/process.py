import os, json
from unicodedata import name

from click import argument
from celery import Celery
from celery.utils.log import get_task_logger
from flask import Blueprint, url_for, render_template, request, jsonify, redirect
from flask_login import login_required, current_user
logger = get_task_logger(__name__)
process = Blueprint('process', __name__)
celery = Celery('task', broker='redis://redis:6379/0')

image_data = ""

@process.route('/sparktask', methods=['GET','POST'])
def sparktask():
    if current_user.is_authenticated:
        spark_job_task.apply_async()
        return url_for('process.loading')
    else:
        return jsonify({'Error': 'User is not authenticated'}), 400

@process.route('/testroute', methods=['GET','POST'])
@login_required
def testroute():
    if request.method == 'POST':
        print("testroute")
        data = json.loads(request.data)
        test_task(data)
        return jsonify({'success': 'true'})

def test_task(data):
    print(json.dumps(data))
    return {'status': 'Task completed!'} 


@process.route('/loading')
@login_required
def loading():
    global image_data
    image_data = ""
    return render_template('loading.html')

@process.route('/updateData', methods=['POST'])
def update_data():
    global image_data
    if not request.form or 'image' not in request.form:
        return "error", 400
    image_data = request.form['image']
    return "success", 201

@process.route('/refreshData')
@login_required
def refresh_data():
    global image_data
    return jsonify(output=image_data)

@process.route('/results', methods=['GET','POST'])
@login_required
def results():
    global image_data
    return render_template('results.html', image_data=image_data)

@celery.task(bind=True)
def spark_job_task(self):

    task_id = self.request.id
    
    master_path = 'spark://spark-master:7077'

    spark_code_path = '/opt/scripts/spark_test.py'

    os.system("~/spark/bin/spark-submit --master %s %s %s" % 
        (master_path, spark_code_path, task_id))

    return {'status': 'Task completed!'} 