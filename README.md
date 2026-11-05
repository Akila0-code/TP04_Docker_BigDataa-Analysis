# TP04: Containerization and Big Data Environment Deployment Using Docker

## 1. Introduction

The objective of this practical work (TP04) is to understand containerization using Docker and to deploy a simple data analysis application in a containerized environment.

Docker allows applications and their dependencies to be packaged into portable containers. This makes applications easier to deploy, execute, and reproduce across different environments.

In this project, Docker is used to analyze a fire monitoring dataset generated for TP03. The project covers Docker image creation, Docker Hub operations, container management, Docker networking, and Docker Compose.

## 2. Project Objectives

The main objectives are:

- Understand the difference between Docker images and containers.
- Build a Docker image using a Dockerfile.
- Upload and download an image from Docker Hub.
- Create and execute multiple containers.
- Create a Docker network to connect containers.
- Use Docker Compose to automate application deployment.
- Analyze a fire monitoring dataset using Python and Pandas.

## 3. Project Structure

The project is organized as follows:

```text
TP04_Docker_BigData/
├── data/
│   └── tp03_fire_monitoring_sample.csv
├── screenshots/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
└── README.md
```

### File descriptions

- `app.py`: Python script that loads and analyzes the dataset.
- `requirements.txt`: Lists the Python dependencies.
- `Dockerfile`: Defines how the Docker image is built.
- `compose.yaml`: Defines the service and its configuration for Docker Compose.
- `data/`: Contains the fire monitoring dataset.
- `screenshots/`: Contains screenshots documenting the execution steps.
- `README.md`: Documents the project and its results.

## 4. Dataset Description

The dataset used in this project is `tp03_fire_monitoring_sample.csv`, generated for the TP03 fire monitoring project.

It contains 10,000 records and seven columns:

| Column | Description |
|---|---|
| `timestamp` | Date and time of the measurement |
| `sensor_id` | Sensor identifier |
| `temperature` | Measured temperature |
| `humidity` | Measured humidity |
| `smoke_level` | Measured smoke level |
| `fire_alarm` | Fire alarm indicator |
| `sensor_status` | Sensor operating status |

The dataset contains 10,000 records, with the following alarm distribution:

- Normal condition (`fire_alarm = 0`): 9,250 records.
- Fire alarm (`fire_alarm = 1`): 750 records.

The dataset is analyzed using Python and the Pandas library.

## 5. Python Data Analysis Application

The application performs the following operations:

1. Loads the CSV dataset.
2. Displays the dataset dimensions and column names.
3. Checks for missing values.
4. Displays the distribution of fire alarm values.
5. Calculates the average temperature, humidity, and smoke level.

The analysis results are:

| Measurement | Result |
|---|---:|
| Number of records | 10,000 |
| Number of columns | 7 |
| Missing values | 0 |
| Normal condition records | 9,250 |
| Fire alarm records | 750 |
| Average temperature | 29.93 |
| Average humidity | 52.69 |
| Average smoke level | 100.50 |

These results confirm that the application successfully loads and analyzes the dataset.

## 6. Docker Image Creation

A Docker image was created to package the Python application and its dependencies.

### 6.1 Dockerfile

The Dockerfile contains the following instructions:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

### 6.2 Explanation of Dockerfile instructions

- `FROM`: Specifies the base image, Python 3.12 slim.
- `WORKDIR`: Sets `/app` as the working directory.
- `COPY`: Copies the required files into the image.
- `RUN`: Installs the Python dependencies.
- `CMD`: Defines the command executed when the container starts.

### 6.3 Build the Docker image

The image was built using:

```powershell
docker build --pull -t tp04-fire-analysis:1.0 .
```

The image contains the Python environment, application code, and required dependencies.

## 7. Docker Hub Operations

The image was uploaded to Docker Hub so that it could be downloaded and reused.

Docker Hub username: `akilasaker`

Repository: `akilasaker/tp04-fire-analysis`

### 7.1 Tag the image

```powershell
docker tag tp04-fire-analysis:1.0 akilasaker/tp04-fire-analysis:1.0
```

### 7.2 Push the image

```powershell
docker push akilasaker/tp04-fire-analysis:1.0
```

### 7.3 Pull the image

```powershell
docker pull akilasaker/tp04-fire-analysis:1.0
```

The push and pull operations completed successfully.

Docker Hub repository: https://hub.docker.com/r/akilasaker/tp04-fire-analysis

## 8. Containers and Docker Networking

Three containers were created from the downloaded Docker image to execute the data analysis application.

The containers were named:

- `tp04-container1`
- `tp04-container2`
- `tp04-container3`

Each container processed the dataset and completed the analysis successfully.

Because the application is a batch-processing program, the analysis containers terminate after finishing their tasks. Therefore, their status is `Exited (0)`, which indicates successful execution.

### 8.1 Create a Docker network

A dedicated network was created using:

```powershell
docker network create tp04-network
```

### 8.2 Create three network-connected containers

Three additional containers were started on the same network to verify that multiple containers could be connected through Docker networking.

```powershell
docker run -d --name tp04-node1 --network tp04-network --entrypoint python akilasaker/tp04-fire-analysis:1.0 -c "import time; time.sleep(3600)"

docker run -d --name tp04-node2 --network tp04-network --entrypoint python akilasaker/tp04-fire-analysis:1.0 -c "import time; time.sleep(3600)"

docker run -d --name tp04-node3 --network tp04-network --entrypoint python akilasaker/tp04-fire-analysis:1.0 -c "import time; time.sleep(3600)"
```

These containers were used to test the network configuration and remain active for a limited period.

### 8.3 Verify the containers and network

```powershell
docker ps
docker network inspect tp04-network
```

The inspection confirmed that the three test containers were connected to `tp04-network`.

No port mapping was required because the application performs local data analysis and does not expose a network service.

## 9. Docker Compose Deployment

Docker Compose simplifies the configuration and execution of applications using a YAML file.

### 9.1 compose.yaml

The following configuration defines the data analysis service:

```yaml
services:
  data-analysis:
    build: .
    container_name: tp04-analysis
    volumes:
      - ./data:/app/data:ro
    restart: "no"
```

### 9.2 Configuration explanation

- `services`: Defines the application services.
- `data-analysis`: Names the service.
- `build: .`: Builds the image using the Dockerfile in the current directory.
- `container_name`: Assigns the name `tp04-analysis` to the container.
- `volumes`: Mounts the local dataset directory into `/app/data`.
- `:ro`: Makes the mounted dataset read-only.
- `restart: "no"`: Prevents automatic restarting after the container exits.

### 9.3 Start the application

```powershell
docker compose up --build
```

Docker Compose built the image and executed the application successfully.

### 9.4 Check the container status

```powershell
docker compose ps -a
```

The container finished with exit code `0`, confirming that the data analysis completed successfully.

### 9.5 Stop and remove the Compose environment

```powershell
docker compose down
```

The container and the default Compose network were removed successfully.

## 10. Questions and Answers

### Question 1: What is Docker, and why is it useful in data science?

Docker is a containerization platform that packages an application and its dependencies into a portable environment.

In data science, Docker is useful because it:

- Provides reproducible execution environments.
- Simplifies dependency management.
- Makes applications easier to deploy.
- Allows the same environment to be used on different machines.
- Supports the execution of multiple isolated containers.

### Question 2: What is the difference between a Docker image and a Docker container?

A Docker image is a packaged template containing the application, its dependencies, and the instructions needed to run it.

A Docker container is a running or stopped instance created from an image.

An image can be used to create multiple containers.

### Question 3: What problem does Docker Compose solve?

Docker Compose simplifies the management of applications by defining their services, configuration, volumes, and networks in a single YAML file.

Instead of manually executing multiple Docker commands, the user can start the configured application using:

```powershell
docker compose up --build
```

### Question 4: What is the difference between `docker run` and `docker compose up`?

`docker run` creates and starts an individual container using command-line options.

`docker compose up` starts the services defined in a Compose configuration file and manages their associated containers and networks.

Docker Compose is particularly useful when an application contains multiple services.

### Question 5: How can a database service be added to Docker Compose?

A database can be added as another service in `compose.yaml`. For example, a PostgreSQL service could be configured as follows:

```yaml
services:
  data-analysis:
    build: .
    volumes:
      - ./data:/app/data:ro
    depends_on:
      - database

  database:
    image: postgres:16
    environment:
      POSTGRES_DB: fire_monitoring
      POSTGRES_USER: analyst
      POSTGRES_PASSWORD: change_me
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

In this example, the analysis service can communicate with PostgreSQL using the hostname `database` on the Compose network. A real deployment should use a secure password, preferably supplied through environment variables or secrets, rather than committing credentials to GitHub.

This example illustrates how Compose can coordinate multiple services; it is an extension of the current project, not a database service already implemented in this TP.

## 11. Conclusion

This practical work introduced Docker containerization and its application to a data analysis project.

A Docker image was built, uploaded to Docker Hub, and downloaded successfully. Multiple containers were created, and a dedicated Docker network was used to connect test containers. Docker Compose was then used to automate the execution of the Python analysis application.

The application successfully analyzed 10,000 fire monitoring records, checked for missing values, displayed the alarm distribution, and calculated the average sensor measurements.

This project demonstrates how Docker improves portability, reproducibility, and deployment management in data science and Big Data environments.
