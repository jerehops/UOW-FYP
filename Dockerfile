FROM python:3.8-slim-buster

RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Define default command
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]