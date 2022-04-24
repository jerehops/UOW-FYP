FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# Define default command
EXPOSE 8000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]