FROM python:3.8-slim-buster

ENV TZ="Asia/Singapore"

RUN apt-get update \
&& apt install unzip \
&& apt install -y default-jdk \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN echo "Install requirements and set up folders"
COPY . .
RUN pip install -r requirements.txt

ADD http://files.grouplens.org/datasets/movielens/ml-latest.zip movie.zip 
RUN unzip -j movie.zip -d movie \
&& rm movie.zip

RUN apt remove unzip -y

# Define default command
EXPOSE 8000