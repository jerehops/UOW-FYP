FROM python:3.8-slim-buster

RUN apt update && \
    apt install -y default-jdk && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Define default command
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]