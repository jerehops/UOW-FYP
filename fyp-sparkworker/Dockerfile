FROM python:3.8-slim-buster

RUN apt update && \
    apt install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /spark
ADD ./scripts/. .
# spark
ADD https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz spark.tgz
RUN tar -xf spark.tgz
RUN rm spark.tgz
RUN mv spark-* spark

EXPOSE 8081
CMD bin/spark-class org.apache.spark.deploy.worker.Worker spark://spark-master:7077 >> logs/spark-worker.out
