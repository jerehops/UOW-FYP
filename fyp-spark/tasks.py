import os
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@app.task()
def spark_job_task(self):
    task_id = self.request.id
    master_path = 'local[2]'
    project_dir = '~/qbox-blog-code/ch_6_toy_saas/'
    jar_path = '~/spark/jars/elasticsearch-hadoop-2.1.0.Beta2.jar'
    spark_code_path =  project_dir + 'es_spark_test.py'
    os.system("~/spark/bin/spark-submit --master %s --jars %s %s %s" % 
        (master_path, jar_path, spark_code_path, task_id))
    return {'current': 100, 'total': 100, 'status': 'Task completed!', 'result': 42} 