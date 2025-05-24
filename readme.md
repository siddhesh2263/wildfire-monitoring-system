# Designing a Real-Time Anomaly Detection System with Kafka, Flask, and K3s
##### Date: 5/24/2025
##### Author: Siddhesh Kocharekar

## Table of Contents

1. [Project Overview](#project-overview)
2. [What is K3s? A Lightweight Kubernetes Engine for Edge and Dev Clusters](#what-is-k3s-a-lightweight-kubernetes-engine-for-edge-and-dev-clusters)
3. [Ingestion with API Gateway](#ingestion-with-api-gateway)
4. [Kafka Messaging](#kafka-messaging)
5. [PostgreSQL Data Storage](#postgresql-data-storage)
6. [Rule-Based Anomaly Detection](#rule-based-anomaly-detection)
7. [Real-Time UI with Leaflet + Flask](#real-time-ui-with-leaflet--flask)
8. [Dockerization and K3s Deployment](#dockerization-and-k3s-deployment)
9. [Load Testing with Locust](#load-testing-with-locust)
10. [Where the System Falls Short: Risks and Limitations](#where-the-system-falls-short-risks-and-limitations)
11. [Next Steps for System Improvement and Production Readiness](#next-steps-for-system-improvement-and-production-readiness)

<br>

### Project Overview

In this project, I designed and deployed a real-time anomaly detection system that simulates environmental hazard reporting. The system ingests continuous data streams (simulated via Locust), performs rule-based anomaly detection, stores incoming and processed data in PostgreSQL, and renders live geospatial alerts on an interactive Leaflet map. Every component is containerized and deployed on a lightweight Kubernetes distribution (K3s), with Kafka acting as the central message broker. The goal was to build a fully functioning pipeline from data ingestion to real-time visualization.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/uml-rough.png?raw=true)

<br>

### What is K3s? A Lightweight Kubernetes Engine for Edge and Dev Clusters

K3s is a lightweight, fully compliant Kubernetes distribution developed by Rancher. It’s optimized for small footprint environments like edge devices, IoT gateways, and development clusters, and it reduces complexity by stripping out unnecessary add-ons and using a single binary for easier installation. Despite its reduced size, K3s still offers the essential features of Kubernetes, such as automated deployment, service discovery, scaling, and load balancing, making it a perfect choice for lightweight, container-based applications like this real-time anomaly detection system.

<br>

### Ingestion with API Gateway

The data ingestion component is a Flask-based API Gateway that accepts POST requests. Incoming JSON payloads are validated and then pushed to a Kafka topic named `raw-data`. Kafka’s asynchronous nature ensures that producers are decoupled from consumers, making the pipeline resilient to downstream slowdowns or failures. The service is also containerized with Docker and deployed on K3s.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/deployments.png?raw=true)

<br>

### Kafka Messaging

Kafka is the backbone of the system, enabling decoupled communication between services. The `raw-data` topic carries raw environmental readings directly from the API Gateway, while a second topic, `anomaly-data`, carries processed messages after risk classification. Topics were manually created using `kafka-topics.sh` inside the Kafka pod deployed on K3s.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kafdrop-messages.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kafdrop-raw-data.png?raw=true)

<br>

### PostgreSQL Data Storage

A dedicated Database Writer service consumes from the `raw-data` topic and writes each entry into a PostgreSQL table. This service connects to the database using `psycopg2`, with credentials securely loaded via a Kubernetes Secret named `pg-secret`. The raw data table includes fields for timestamp, geolocation, temperature, humidity, wind conditions, and other metadata.

<br>

### Rule-Based Anomaly Detection

An anomaly detection service consumes messages from the `raw-data` topic and applies rule-based logic to assign an intensity label—low, medium, or high. For example, if the temperature exceeds 40°C and humidity drops below 20%, the message is tagged as a high-risk anomaly. Additional rules consider vegetation density, wind speed, and air quality index. The service adds a confidence_score and produces the data into the `anomaly-data` topic. This service is stateless, horizontally scalable, and containerized like all others.

<br>

### Real-Time UI with Leaflet + Flask

To visualize the detected anomalies, I built a UI service using Flask and Leaflet. The backend continuously consumes from the `anomaly-data` Kafka topic and buffers the latest messages in memory using a deque. A `/data` API endpoint returns this buffered data in JSON format, which the frontend JavaScript fetches every 5 seconds. The Leaflet map displays color-coded markers based on intensity: red for high, orange for medium, and yellow for low. Each marker includes a popup with geolocation, timestamp, and confidence score. This setup delivers a near real-time visualization of environmental anomalies.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/map-main-marker.png?raw=true)

<br>

### Dockerization and K3s Deployment

Each microservice in the system was packaged in its own Docker container with a corresponding `requirements.txt` and `Dockerfile`. I used Docker Hub to load these images into the K3s cluster. Kubernetes Deployment and Service YAMLs were written for each service, allowing me to manage replica counts, port exposure, and environment variables in a clean, declarative manner. K3s was chosen for its simplicity and lightweight footprint, making it easier for development.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/nodes-all.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/pods-lens.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kubectl-pods-wide.png?raw=true)

<br>

### Load Testing with Locust

To validate the ingestion pipeline and measure system performance under realistic load, I used Locust, an open-source load testing framework that simulates multiple concurrent users sending HTTP requests. Locust allowed me to easily generate a sustained load of `200–300` requests per second to the API Gateway, replicating the real-world scenario of sensors or edge devices continuously reporting environmental data.

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/locust-main.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/locust-chart.png?raw=true)

<br>

### Where the System Falls Short: Risks and Limitations

While the system demonstrates real-time data ingestion and visualization, it has major reliability gaps. Kafka is single-node and unreplicated, risking total data loss on failure. K3s uses SQLite, unsuitable for HA workloads, making control plane failure catastrophic. No resource limits risk CPU throttling, and consumers lack retry or dead-letter queues, causing permanent data loss if a write or anomaly detection fails. The UI’s in-memory buffer can’t recover from restarts, leading to silent data gaps. With no observability tools like Prometheus or logs, these issues remain hidden. No authentication or TLS, plus no chaos testing, leaves the system unproven in production.

<br>

### Next Steps for System Improvement and Production Readiness

To improve the system’s reliability and prepare it for production, several key upgrades should be implemented. Replace the single-node Kafka deployment with a multi-broker, replicated cluster using Strimzi or Bitnami Helm charts to ensure durability and failover. Upgrade the K3s control plane to an HA configuration with embedded etcd, providing consistent API availability even if a node fails. Enhance consumer resilience by adding retry logic and dead-letter queues to the Database Writer and Anomaly Detection services, ensuring data integrity during transient failures. For UI reliability, replace in-memory buffers with persistent caching in Redis or database queries to maintain live visualization after restarts. Implement Prometheus and Grafana to collect metrics on request latency, Kafka lag, and database performance, enabling proactive monitoring and alerting. Define resource requests and limits for pods and enable autoscaling for key services. Finally, introduce TLS encryption for Kafka and PostgreSQL and perform chaos testing to validate the system’s resilience and real-world stability.