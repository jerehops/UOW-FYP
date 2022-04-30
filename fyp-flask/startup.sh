#! /bin/bash

celery -A app.process worker --loglevel=info
flask run