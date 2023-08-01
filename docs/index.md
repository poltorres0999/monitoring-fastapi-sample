# Monitoring FastAPI Applications with Promtail, Loki, Grafana, and Prometheus

## Table of contents

- [Introduction](#introduction)
- [What are we actually building](#what-are-we-actually-building)
- [How it Works](#how-it-works)
- [Installation](#installation)
- [Configurations in depth](#configurations-in-depth)
    - [Prometheus](#prometheus)
    - [Promtail](#promtail)
    - [Loki](#loki)
    - [Grafana IAC](#grafana-iac)
      
## Introduction

Welcome to the Monitoring FastAPI Applications project! This repository provides a simple and practical implementation of monitoring a FastAPI application using popular open-source monitoring tools: Promtail, Loki, Grafana, and Prometheus. The goal of this project is to showcase an effective monitoring setup that helps you gain insights into your FastAPI application's logs and metrics, enabling you to identify and troubleshoot issues quickly.

Monitoring plays a crucial role in ensuring the health, performance, and reliability of web applications. With this setup, you'll be able to collect logs, track metrics, visualize data, and set up alerts for potential issues in your FastAPI application. The monitoring stack consists of the following components:

- **Promtail:** A lightweight log collector specifically designed to work with Loki. It efficiently gathers logs from your FastAPI application's containers and forwards them to Loki for storage and analysis.

- **Loki:** A horizontally scalable, multi-tenant log aggregation system. It enables you to query, filter, and analyze logs in real-time using powerful LogQL queries.

- **Grafana:** A popular open-source platform for monitoring and observability. Grafana is used to create rich dashboards and visualizations based on the data from Loki and Prometheus.

- **Prometheus:** A powerful time-series database and monitoring system. It collects and stores metrics exposed by the FastAPI application and other services, allowing you to set up custom alerts and recording rules, the date stored could be extracted by using its custom queryng languge PromQL.

## What are we actually building
The primary objective is to create a straightforward yet informative dashboard that offers valuable insights into the application's status. This dashboard will serve as a convenient tool to organize and present the most relevant logs, providing a quick overview of the application's health and performance.

![Example Image](/images/general_stats.PNG)
![Example Image](/images/requests1.PNG)
![Example Image](/images/requests2.PNG)
![Example Image](/images/logs.PNG)

## How it Works

![Example Image](/images/monitoring_schema.png)

The monitoring setup relies on Docker and Docker Compose to manage the deployment of the services. You will use the provided `docker-compose.yml` file to orchestrate the entire monitoring stack.

- **FastAPI Application:** You'll start by creating and running a simple FastAPI application. This application will consist of several endpoints, including multiple types of HTTP requests (GET, POST, PUT, DELETE), and it will serve as an example web service that we want to monitor. The FastAPI application is equipped with a Prometheus instrumentator that will be responsible for generating the performance metrics exposed at the **"/metrics"** endpoint.

- **Promtail:** Promtail will be in charge of scraping, labeling and forwarding the logs to Loki, by sending them to the Loki's exposed enpoint **http://loki:3100/loki/api/v1/push**. The logs will be acquiered by scraping the files at **/var/logs/\*.log"** which will be provisoned to the container Promtail service container through a Docker volume. Promtail will be configured by making use of the `promtail-config.yaml`. 

- **Loki:** Loki will serve as the logs data source, wich will be consumed by Grafana at **http://loki:3100**. Loki will be configured by making use of the `loki-config.yaml`. 

- **Prometheus:** Prometheus will act as the data source for Grafana to retrieve the FastAPI App metrics at **http://prometheus:9090**. These metrics will be acquired by periodically consulting the exposed "/metrics" endpoint at the FastAPI App. Prometheus will be configured by making use of the `prometheus.yaml`. 

- **Grafana:** Grafana will be used to visualize logs and metrics from Loki and Prometheus. The required dashboard configuration and Datasources will be provisioned as **IAC** (Infrastrucutre as a Code) the files in chage of doing so can be found at **/grafana/config/dashboards** and **/grafana/config/datasources**

- **API metrics generator:** The `metrics/api_metrics_generator.py` file consists of a python scripts that periodically queries several endpoints of the FastAPI App to trigger the generation of metrics by the prometheus instrumentator.

- **API Log Generator:** The `metrics/log_generator.py` file consists of a python scripts that populates the logs folder with several files with fake logs.

## Installation

To get started with monitoring your FastAPI application using Promtail, Loki, Grafana, and Prometheus, follow the steps below to set up the required tools and services:

**Step 1: Install Docker**

Docker is a containerization platform that allows you to run applications and services in isolated containers. It's a fundamental requirement for this monitoring setup.

Follow the official [Docker installation guide](https://docs.docker.com/engine/install/) for your specific operating system:

After installing Docker, make sure it's running by executing the following command:
```bash
    docker-compose --version
```

**Step 2: Install Docker Compose**

Docker Compose is a tool for defining and running multi-container Docker applications using a docker-compose.yml file.

Follow the official [Docker Compose installation](https://docs.docker.com/compose/install/) guide for your specific operating system:

Install Docker Compose
Verify the installation by checking the version of Docker Compose:
```bash
    docker-compose --version
```

**Step 3: Clone the Repository**

Next, clone the Monitoring FastAPI Applications repository to your local machine:
```
    git clone https://github.com/poltorres0999/monitoring-fastapi-sample.git
    cd monitoring-fastapi-sample
```

**Step 4: Start the monitoring Stack**

To initiate the monitoring stack, execute the following command. Since everything is configured as Infrastructure as Code (IAC), all the necessary services will be automatically set up and deployed, including the log and metrics generation scripts. This seamless process ensures a hassle-free setup of the entire monitoring ecosystem.
```bash
    docker-compose up
```

**Step 5: Check that everything is up and running**

Go to http://localhost:3000 wich will open the Grafan application, log in using the default user and password admin:admin, once logged in
navigate to Dashboards >> Fast API Metrics >> Fast API Metrics POC. It should show a dashboard similar to the one presented at [What are we actually building](#what-are-we-actually-building).

## Configurations in depth
### Prometheus
```yml
# File: prometheus.yml
# Global configuration settings applicable to all scrape jobs
global:
  scrape_interval: 15s  # The interval at which Prometheus scrapes metrics from targets (e.g., 15 seconds)

# Scrape configurations for individual jobs
scrape_configs:
  - job_name: "fastapi"  # The name of the job, used to identify the metrics collected from this target

    # Static configuration for this job, where targets are explicitly defined
    static_configs:
      - targets: ["fast-api-metrics-test:8000"]  # The hostname and port of the target where the metrics are exposed
```
**global**: 
The global section sets global configurations, including the `scrape_interval`, which defines the time interval between Prometheus scraping data from targets. In this case, it's set to 15 seconds.


**scrape_configs**:
The `scrape_configs` section is a list of scrape configurations for individual jobs.

- **job_name: "fastapi"**:
  Inside the `scrape_configs`, there is one job defined with the name "fastapi". This is the name that Prometheus will use to identify the metrics collected from this target.

  - **static_configs**:
    Within the job, there is a `static_configs` section, where the targets are specified. In this case, the target is "fast-api-metrics-test:8000", which represents the hostname and port of the target where the metrics are exposed. Prometheus will scrape metrics from this target according to the defined `scrape_interval`.
    
### Promtail
```yaml
# Server configurations
server:
  http_listen_port: 9080  # HTTP port on which Promtail will listen for requests
  grpc_listen_port: 0     # gRPC port, set to 0 to disable gRPC

# Loki client configuration
clients:
  - url: http://loki:3100/loki/api/v1/push
    # The URL where Loki's /loki/api/v1/push endpoint is located. Promtail will push logs to this endpoint.

# Positions file configuration
positions:
  filename: /tmp/positions.yaml
  # The file that stores the last positions of log files read by Promtail. Used for log persistence and resume.

# Scrape configurations for log processing
scrape_configs:
  - job_name: system  # The name of the job, used to identify the log processing pipeline for this target.

    # Pipeline stages for log processing
    pipeline_stages:
      # Regex stage to extract log components using named capture groups
      - regex:
          expression: '^(?P<log_timestamp>[\d-]+T[\d:.]+Z) \| (?P<log_level>\w+) \| Module: (?P<module>[^|]+) \| Function: (?P<function>[^|]+)\| (?P<message>.*)'
          # Regular expression used to extract log components: timestamp, log_level, module, function, message

      # Labels stage to define custom labels for the extracted log components
      - labels:
          log_level:   # Custom label "log_level" mapped to the extracted "log_level" from the regex stage
          module:      # Custom label "module" mapped to the extracted "module" from the regex stage
          function:    # Custom label "function" mapped to the extracted "function" from the regex stage

      # Timestamp stage to parse and set the timestamp from the extracted "log_timestamp"
      - timestamp:
          source: log_timestamp
          format: "RFC3339"
          # Parsing the "log_timestamp" field and setting it as the timestamp in RFC3339 format

      # Another regex stage to extract more log components using named capture groups
      - regex:
          expression: '^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z) \| (?P<log_level>\w+) \| (?P<method>\w+) (?P<uri>[^\s]+) \| Requested by: (?P<requested_by>[^|]+) Status: (?P<status>\d+) Duration: (?P<duration>\d+) ms'
          # Regular expression used to extract log components: timestamp, log_level, method, uri, requested_by, status, duration

      # Labels stage to define custom labels for the extracted log components
      - labels:
          log_level:   # Custom label "log_level" mapped to the extracted "log_level" from the regex stage
          method:      # Custom label "method" mapped to the extracted "method" from the regex stage
          uri:         # Custom label "uri" mapped to the extracted "uri" from the regex stage
          status:      # Custom label "status" mapped to the extracted "status" from the regex stage

      # Timestamp stage to parse and set the timestamp from the extracted "timestamp"
      - timestamp:
          source: log_timestamp
          format: "RFC3339"
          # Parsing the "log_timestamp" field and setting it as the timestamp in RFC3339 format

    # Static configurations for this job, specifying the targets and labels
    static_configs:
      - targets:
          - localhost  # The target from where logs are read. In this case, logs are read from the local machine.
        labels:
          job: fast-api-logs  # Custom label "job" mapped to "fast-api-logs" to identify this job in Loki
          env: dev           # Custom label "env" mapped to "dev" indicating the environment where the logs come from
          __path__: /var/log/logs.log  # The path to the log file that Promtail should scrape

```
**Server Configuration**
Defines the ports on which Promtail listens for incoming requests. The `http_listen_port` is set to 9080, enabling Promtail to accept HTTP requests. The `grpc_listen_port` is set to 0, which disables the gRPC server.

**Loki Client Configuration**
Specifies the URL of the Loki server's `/loki/api/v1/push` endpoint. Promtail will push the processed logs to this endpoint for storage in Loki.

**Positions Configuration**
Specifies the filename where Promtail will store the positions of the log files it has read. This enables Promtail to resume reading logs from where it left off in case of restarts.

**Scrape Configurations for Log Processing**
Defines the log processing pipeline for the specified job, which is named "system" in this case.

**Pipeline Stages for Log Processing**
The configuration defines multiple pipeline stages to extract relevant information from the log lines using regular expressions (regex). The extracted components include `log_timestamp`, `log_level`, `module`, `function`, `message`, `method`, `uri`, `requested_by`, `status`, and `duration`.

**Labels for Log Components**
Custom labels are defined for each extracted log component to be used for efficient indexing and querying in Loki.

**Timestamp Parsing**
Timestamps are extracted from the log lines and converted to the RFC3339 format to be used as the timestamp for the log entries in Loki.

**Static Configurations**
Specifies the targets (log file paths) from where Promtail will read logs. In this configuration, logs are read from the file `/var/log/logs.log` on the local machine (localhost). The custom labels `job` and `env` are assigned values "fast-api-logs" and "dev," respectively, to provide additional metadata about the logs.

### Loki
```
# Authentication Configuration
auth_enabled: false
# Indicates whether authentication is enabled or not. In this case, it's set to false.

# Server Configuration
server:
  http_listen_port: 3100
# Configures the HTTP port on which the Loki server listens for incoming requests.

# Limits Configuration
limits_config:
  max_cache_freshness_per_query: "10m"
  # The maximum time range for cache freshness allowed per query is set to 10 minutes.

  split_queries_by_interval: 24h
  # Queries are split into 24-hour intervals to parallelize query execution.

  reject_old_samples: true
  # Old samples (out of the retention period) are rejected from being ingested.

  reject_old_samples_max_age: 168h
  # Defines the maximum age (168 hours or 7 days) of samples before they are rejected.

  retention_period: 360h
  # The retention period for logs is set to 360 hours or 15 days.

  max_query_series: 2500
  # Limits the maximum number of series that a single query can match to 2500.

  max_query_parallelism: 2
  # Limits the maximum number of concurrent queries that can be executed in parallel to 2.

# Frontend Configuration
frontend:
  max_outstanding_per_tenant: 2048
  # Limits the number of outstanding requests per tenant to 2048.

# Query Scheduler Configuration
query_scheduler:
  max_outstanding_requests_per_tenant: 2048
  # Limits the number of outstanding requests per tenant in the query scheduler to 2048.
  
  ...
```
- **Authentication Configuration**: Indicates whether authentication is enabled or not. In this case, it's set to false, meaning no authentication is required.

- **Server Configuration**: Configures the HTTP port on which the Loki server listens for incoming requests. It's set to listen on port 3100.

- **Limits Configuration**: Defines various configuration parameters for performance and resource usage control, such as cache freshness, query splitting, rejection of old samples, retention period, maximum query series, and maximum query parallelism.

    - **max_cache_freshness_per_query:** Specifies the maximum time range for cache freshness allowed per query. In this case, it's set to 10 minutes (10m). This limits how far back in time cached data can be used for a single query.

    - **split_queries_by_interval:** Queries are split into intervals to parallelize query execution. In this case, it's set to 24 hours (24h). This means that queries are broken into 24-hour intervals to be executed in parallel, improving query performance.

    - **reject_old_samples:** When set to true, it enables the rejection of old samples (logs) that fall outside the retention period. Old samples are not ingested into the system.

    - **reject_old_samples_max_age:** Specifies the maximum age of samples (logs) before they are rejected from ingestion. In this case, it's set to 168 hours (168h), which is equivalent to 7 days.

    - **retention_period:** Sets the retention period for log data. In this case, it's set to 360 hours (360h), which is equivalent to 15 days. Logs older than the retention period will be automatically removed from Loki.

    - **max_query_series:** Limits the maximum number of series (streams of logs) that a single query can match. In this case, it's set to 2500, which restricts the number of log streams returned by a query.

    - **max_query_parallelism:** Sets the maximum number of concurrent queries that can be executed in parallel. In this case, it's set to 2, which limits the number of queries Loki can process simultaneously.

- **Frontend Configuration**: Sets a limit for the number of outstanding (pending) requests per tenant (user) in the Loki frontend to 2048.

- **Query Scheduler Configuration**: Limits the number of outstanding (pending) requests per tenant in the query scheduler to 2048.

### Grafana IAC

Even though the Grafana service is being created with its default configuration, it is essential to highlight the significant role of Infrastructure as Code (IAC) in the provisioning of dashboards and datasources for the Fast API Metrics dashboard. By adopting the principles of IAC, we treat infrastructure components like dashboards and datasources as code artifacts, enabling us to manage and version control these resources systematically.

The dashboard and datasources that constitute the Fast API Metrics dashboard are defined and maintained as code. This practice ensures consistency, reproducibility, and automation in managing these vital components of our monitoring infrastructure. Any changes made to the dashboards or datasources are recorded and tracked in version control systems, allowing for easy collaboration among team members and simplifying the process of rolling back to previous configurations if needed.

The configuration files that define these resources are stored at `/grafana/config/dashboards` for dashboards and `/grafana/config/datasources` for datasources, and provisioned to the Grafa service throguh a Docker volume, ensuring that they are readily accessible and can be deployed consistently across different environments.
