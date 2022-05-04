FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN mkdir -p /opt/scripts \
&& mv spark_test.py /opt/scripts/spark_test.py

RUN wget https://files.grouplens.org/datasets/movielens/ml-latest.zip -O movie.zip \
&& unzip movie.zip -j -d movie \
&& rm movie.zip

# Define default command
EXPOSE 8000