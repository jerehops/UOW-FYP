FROM python:3.8-slim-buster

RUN echo "Setting app directory"
WORKDIR /app
RUN echo "Setting app directory"

RUN echo "Install requirements and set up folders"
COPY . .
RUN pip install -r requirements.txt

RUN echo "Make directories"
RUN mkdir -p opt/scripts \
&& mkdir -p opt/data/default

RUN echo "Moving files"
RUN mv ./scripts/spark_test.py opt/scripts


WORKDIR /opt/data/default

RUN wget https://files.grouplens.org/datasets/movielens/ml-latest.zip -O movie.zip \
&& unzip movie.zip -j -d movie \
&& rm movie.zip

# Define default command
EXPOSE 8000