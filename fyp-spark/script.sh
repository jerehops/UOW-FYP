#! /bin/bash

../spark/spark/sbin/start-master.sh

celery -A tasks worker --loglevel=info
