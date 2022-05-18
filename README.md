
# Containerisation of Big Data Architecture
*Flask front end with elasticsearch as RDD and spark for data processing*
### Docker Repository
*For latest docker images kindly head to the URLs below to check*
 - [Flask (Frontend)](https://hub.docker.com/repository/docker/jerehops/fyp-flask)
 - [Spark (Backend)](https://hub.docker.com/repository/docker/jerehops/fyp-spark)
### Prerequisites

 - Install [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)


### Download from Docker Hub (easier)

1. Download the fullstack-deployment folder;

```bash
curl https://raw.githubusercontent.com/jerehops/fyp/main/deployment/docker-compose.yaml -O 

```

2. Start the cluster (Please use docker compose 2);

```bash
docker compose up

```
If this doesn't work, add Sudo .
```bash
sudo docker compose up

```

