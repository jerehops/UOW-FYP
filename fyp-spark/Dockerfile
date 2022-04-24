FROM python:3.8-slim-buster

RUN apt update && \
    apt install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /spark
# spark
ADD https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz ./spark.tgz
RUN tar -xf ./spark.tgz
RUN rm ./spark.tgz
RUN mv spark-* spark
COPY ./jars ./jars

#COPY app.py /app.py
WORKDIR /simple_worker
ADD ./tasks.py .

EXPOSE 8080 7077
CMD ["/bin/bash", "celery -A tasks worker --loglevel=info"]