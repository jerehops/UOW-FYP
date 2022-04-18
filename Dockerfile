FROM ubuntu:latest

WORKDIR /app

COPY . .

RUN \
  apt-get update && \
  apt-get install -y openjdk-8-jdk && \
  rm -rf /var/lib/apt/lists/*

# Install Python
RUN \
    apt-get update && \
    apt-get install -y install python3.8 && \
    rm -rf /var/lib/apt/lists/*

# Install PySpark and Numpy
RUN \
    pip install --upgrade pip && \
    pip install pyspark

RUN pip install -r requirements.txt

# Define default command
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]