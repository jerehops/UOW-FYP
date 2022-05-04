FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt \
&& mkdir -p /opt/scripts \
&& mkdir -p opt/data/default

WORKDIR /opt/scripts
RUN mv ./app/spark_test.py ./opt/scripts/spark_test.py

WORKDIR /opt/data/default

RUN wget https://files.grouplens.org/datasets/movielens/ml-latest.zip -O movie.zip \
&& unzip movie.zip -j -d movie \
&& rm movie.zip

# Define default command
EXPOSE 8000