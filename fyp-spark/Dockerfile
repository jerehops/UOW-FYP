FROM python:3.8-slim-buster

ENV TZ="Asia/Singapore"

RUN apt update && \
    apt install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

# spark
ADD https://dlcdn.apache.org/spark/spark-3.2.1/spark-3.2.1-bin-hadoop3.2.tgz spark.tgz
RUN mkdir -p /opt/spark \
&& tar -xf spark.tgz -C /opt/spark --strip-components=1 \
&& rm spark.tgz

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /opt/spark/bin

CMD ["/bin/bash", "/opt/spark/bin/start-spark.sh"]
