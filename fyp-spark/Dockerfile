FROM python:3.8-slim-buster

COPY requirements.txt .

RUN apt update && \
    pip install -r /requirements.txt && \
    apt install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /spark


# spark
ADD https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz spark.tgz
RUN tar -xf spark.tgz
RUN rm spark.tgz
RUN mv spark-* spark

EXPOSE 8080 7077
CMD bin/spark-class org.apache.spark.deploy.master.Master >> logs/spark-master.out