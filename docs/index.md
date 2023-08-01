Monitoring FastAPI Applications with Promtail, Loki, Grafana, and Prometheus

## Introduction

Welcome to the Monitoring FastAPI Applications project! This repository provides a simple and practical implementation of monitoring a FastAPI application using popular open-source monitoring tools: Promtail, Loki, Grafana, and Prometheus. The goal of this project is to showcase an effective monitoring setup that helps you gain insights into your FastAPI application's logs and metrics, enabling you to identify and troubleshoot issues quickly.

Monitoring plays a crucial role in ensuring the health, performance, and reliability of web applications. With this setup, you'll be able to collect logs, track metrics, visualize data, and set up alerts for potential issues in your FastAPI application. The monitoring stack consists of the following components:

1. **Promtail:** A lightweight log collector specifically designed to work with Loki. It efficiently gathers logs from your FastAPI application's containers and forwards them to Loki for storage and analysis.

2. **Loki:** A horizontally scalable, multi-tenant log aggregation system. It enables you to query, filter, and analyze logs in real-time using powerful PromQL queries.

3. **Grafana:** A popular open-source platform for monitoring and observability. Grafana is used to create rich dashboards and visualizations based on the data from Loki and Prometheus.

4. **Prometheus:** A powerful time-series database and monitoring system. It collects and stores metrics exposed by the FastAPI application and other services, allowing you to set up custom alerts and recording rules.

## What are we actually building
The primary objective is to create a straightforward yet informative dashboard that offers valuable insights into the application's status. This dashboard will serve as a convenient tool to organize and present the most relevant logs, providing a quick overview of the application's health and performance.

![Example Image](docs/images/general_stats.PNG)
![Example Image](docs/images/requests1.PNG)
![Example Image](docs/images/requests2.PNG)
![Example Image](docs/images/logs.PNG)

## How it Works

![Example Image](docs/images/monitoring_schema.png)

The monitoring setup relies on Docker and Docker Compose to manage the deployment of the services. You will use the provided `docker-compose.yml` file to orchestrate the entire monitoring stack.

1. **FastAPI Application:** You'll start by creating and running a simple FastAPI application. This application will serve as an example web service that we want to monitor.

2. **Promtail Configuration:** The `promtail-config.yaml` file specifies how Promtail collects logs from the FastAPI application's containers.

3. **Loki Configuration:** The `loki-config.yaml` file defines the configuration for Loki, including the storage and retention settings.

4. **Grafana Dashboard:** Grafana will be used to visualize logs and metrics from Loki and Prometheus. The `grafana-storage` volume is used to persist Grafana data.

5. **Prometheus Configuration:** The `prometheus.yml` file defines the metrics to scrape from the FastAPI application and other services.

6. **API metrics generator:** The `metrics/api_metrics_generator.py` file consists of a python scripts that periodically queries several endpoints of the FastAPI App to trigger the generation of metrics by the prometheus instrumentator.

5. **API Log Generator:** The `metrics/log_generator.py` file consists of a python scripts that populates the logs folder with several files with fake logs.

## Installation
To get started with monitoring your FastAPI application using Promtail, Loki, Grafana, and Prometheus, follow the steps below to set up the required tools and services:

1. **Install Docker**

Docker is a containerization platform that allows you to run applications and services in isolated containers. It's a fundamental requirement for this monitoring setup.

Follow the official [Docker installation guide](https://docs.docker.com/engine/install/) for your specific operating system:

After installing Docker, make sure it's running by executing the following command:
```bash
    docker-compose --version
```

2. **Install Docker Compose**

Docker Compose is a tool for defining and running multi-container Docker applications using a docker-compose.yml file.

Follow the official [Docker Compose installation](https://docs.docker.com/compose/install/) guide for your specific operating system:

Install Docker Compose
Verify the installation by checking the version of Docker Compose:
```bash
    docker-compose --version
```

3. **Clone the Repository**

Next, clone the Monitoring FastAPI Applications repository to your local machine:
```
    git clone https://github.kyndryl.net/EXPLO/fast-api-metrics-test.git
    cd fast-api-metrics-test
```

4. **Start the monitoring Stack**

To initiate the monitoring stack, execute the following command. Since everything is configured as Infrastructure as Code (IAC), all the necessary services will be automatically set up and deployed, including the log and metrics generation scripts. This seamless process ensures a hassle-free setup of the entire monitoring ecosystem.
```bash
    docker-compose up
```

5. **Check that everything is up and running**

Go to http://localhost:3000 wich will open the Grafan application, log in using the default user and password admin:admin, once logged in
navigate to Dashboards >> Fast API Metrics >> Fast API Metrics POC. It should show a dashboard similar to the one presented at [What are we actually building](#what-are-we-actually-building).
