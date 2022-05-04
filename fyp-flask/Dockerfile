FROM python:3.8-slim-buster

RUN apt-get update && \
apt install unzip

WORKDIR /app

RUN echo "Install requirements and set up folders"
COPY . .
RUN pip install -r requirements.txt

RUN echo "Make directories"
RUN mkdir -p opt/scripts \
&& mkdir -p opt/data/default

RUN echo "Moving files"
RUN mv ./scripts/spark_test.py opt/scripts

ADD https://files.grouplens.org/datasets/movielens/ml-latest.zip movie.zip 
RUN unzip -j movie.zip -d movie \
&& rm movie.zip

RUN apt remove unzip -y

# Define default command
EXPOSE 8000