FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Define default command
EXPOSE 8000
ENTRYPOINT ["/bin/bash", "./startup.sh"]