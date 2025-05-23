## 5/23/2025

## Designing a Real-Time Anomaly Detection System with Kafka, Flask, and K3s

### Project Overview

* In this project, I designed and deployed a real-time anomaly detection system that simulates environmental hazard reporting. The system ingests continuous data streams (simulated via Locust), performs rule-based anomaly detection, stores incoming and processed data in PostgreSQL, and renders live geospatial alerts on an interactive Leaflet map. Every component is containerized and deployed on a lightweight Kubernetes distribution (K3s), with Kafka acting as the central message broker. The goal was to build a fully functioning pipeline from data ingestion to real-time visualization

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/map-main-marker.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/nodes-all.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/pods-lens.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/replica-sets.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/locust-main.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/locust-chart.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kafdrop.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kafdrop-raw-data.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/deployments.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kafdrop-messages.png?raw=true)

![alt text](https://github.com/siddhesh2263/wildfire-monitoring-system/blob/main/assets/kubectl-pods-wide.png?raw=true)