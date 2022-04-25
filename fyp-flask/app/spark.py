import os
import random
import time
from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for, jsonify
from datetime import datetime
from celery import Celery
from elasticsearch import Elasticsearch

spark = Blueprint('main', __name__)

# Celery configuration
celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


ELASTIC_PASSWORD = "Qwerty@sd123"

es = Elasticsearch("https://es01:9200", ca_certs="ca.crt", basic_auth=("elastic", ELASTIC_PASSWORD))   


@spark.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@spark.route('/sparktask', methods=['POST'])
def sparktask():
    task = spark_job_task.apply_async()

    if not es.indices.exists('spark-jobs'):
        print("creating '%s' index..." % ('spark-jobs'))
        res = es.indices.create(index='spark-jobs', body={
            "settings" : {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        })
        print(res)

    es.index(index='spark-jobs', doc_type='job', id=task.id, body={
        'current': 0, 
        'total': 100,
        'status': 'Spark job pending..',
        'start_time': datetime.utcnow()
    })

    return jsonify({}), 202, {'Location': url_for('taskstatus', task_id=task.id)}


@spark.route('/status/<task_id>')
def taskstatus(task_id, methods=['GET']):
    
    task = spark_job_task.AsyncResult(task_id)

    if task.state == 'FAILURE':
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    else:
        # otherwise get the task info from ES
        es_task_info = es.get(index='spark-jobs',doc_type='job',id=task_id)
        response = es_task_info['_source']
        response['state'] = task.state

    return jsonify(response)


@celery.task(bind=True)
def spark_job_task(self):

    task_id = self.request.id

    master_path = 'spark://spark-master:7077'

    project_dir = '/spark'

    jar_path = '/spark/jars/elasticsearch-hadoop.jar'

    spark_code_path =  project_dir + '/es_spark_test.py'

    os.system("~/spark/bin/spark-submit --master %s --jars %s %s %s" % 
        (master_path, jar_path, spark_code_path, task_id))

    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42} 
