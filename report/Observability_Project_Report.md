# Complete Observability System
## Project Report

---

## 1. Project Title

**Complete Observability System using Prometheus, Grafana, Loki, Promtail and Jaeger**

---

## 2. Introduction

Observability is the ability to understand the internal state and behavior of an application by analyzing its metrics, logs, and traces.

This project implements a complete local observability system for a containerized Flask application. The system uses Docker Compose to run the application together with Prometheus, Grafana, Loki, Promtail, and Jaeger.

The project demonstrates the three major pillars of observability:

- Metrics
- Logs
- Traces

Grafana provides a centralized visualization interface for monitoring application metrics and logs, while Jaeger is used for distributed tracing.

---

## 3. Problem Statement

Modern applications consist of multiple services and generate large amounts of operational data.

Without a centralized observability solution, it can be difficult to:

- Monitor application performance.
- Identify failed HTTP requests.
- Analyze application logs.
- Detect errors.
- Investigate application behavior.
- Understand request activity over time.
- Trace requests across services.

Therefore, this project implements an integrated observability stack that collects, stores, queries, and visualizes application metrics, logs, and traces.

---

## 4. Objectives

The objectives of this project are:

1. Develop and containerize a Flask application.
2. Expose application metrics in Prometheus format.
3. Collect application metrics using Prometheus.
4. Collect Docker container logs using Promtail.
5. Store centralized logs using Loki.
6. Visualize metrics and logs using Grafana.
7. Implement distributed tracing using Jaeger.
8. Monitor HTTP request activity.
9. Monitor successful and failed HTTP requests.
10. Demonstrate error detection and troubleshooting using observability tools.
11. Integrate all components using Docker Compose.

---

## 5. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Flask | Web application framework |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Prometheus | Metrics collection |
| Grafana | Metrics and log visualization |
| Loki | Centralized log storage |
| Promtail | Log collection |
| Jaeger | Distributed tracing |
| Git | Version control |
| PowerShell | Project management and Docker commands |

### Component Versions

| Component | Version |
|---|---|
| Grafana | 12.1.1 |
| Prometheus | 3.5.0 |
| Loki | 3.5.0 |
| Promtail | 3.5.0 |
| Jaeger | 1.76.0 |

---

## 6. System Architecture

The system follows an observability pipeline in which the Flask application generates metrics, logs, and traces.

### Architecture Flow

    +-----------------------+
    |   Flask Application   |
    |       Port 5000       |
    +-----------+-----------+
                |
       +--------+--------+
       |        |        |
       v        v        v
 Prometheus  Promtail   Jaeger
    |           |
    |           v
    |          Loki
    |           |
    +-----+-----+
          |
          v
      +---------+
      | Grafana |
      |  :3001  |
      +---------+

### Data Flow

**Metrics:**

    Flask Application → Prometheus → Grafana

**Logs:**

    Docker Container → Promtail → Loki → Grafana

**Traces:**

    Flask Application → Jaeger

This architecture provides centralized visibility into application behavior.

---

## 7. Project Structure

    complete-observability-system/
    │
    ├── app/
    │   ├── app.py
    │   ├── Dockerfile
    │   └── requirements.txt
    │
    ├── grafana/
    │   ├── dashboards/
    │   └── provisioning/
    │       ├── dashboards/
    │       └── datasources/
    │
    ├── loki/
    │   └── loki-config.yml
    │
    ├── prometheus/
    │   └── prometheus.yml
    │
    ├── promtail/
    │   └── promtail-config.yml
    │
    ├── screenshots/
    │
    ├── report/
    │   └── Observability_Project_Report.md
    │
    ├── .gitignore
    ├── docker-compose.yml
    └── README.md

---

## 8. Application Endpoints

The Flask application provides the following endpoints:

| Endpoint | Purpose |
|---|---|
| `/` | Home endpoint |
| `/health` | Application health check |
| `/api/data` | Data API |
| `/api/error` | Intentional error generation |
| `/metrics` | Prometheus metrics |

The `/api/error` endpoint is intentionally used to generate an HTTP 500 response so that error monitoring can be demonstrated.

---

## 9. Docker Compose Configuration

Docker Compose is used to manage all components of the observability system.

The following services are configured:

1. Flask Application
2. Prometheus
3. Loki
4. Grafana
5. Promtail
6. Jaeger

All services communicate through a shared Docker bridge network named:

    observability

Persistent Docker volumes are used for:

    prometheus_data
    loki_data
    grafana_data

---

## 10. Flask Application

The Flask application acts as the monitored application.

It provides normal application endpoints, health checks, metrics, and an intentional error endpoint.

Example successful requests include:

    GET / HTTP/1.1 200

    GET /health HTTP/1.1 200

    GET /api/data HTTP/1.1 200

The application also generates an intentional error:

    GET /api/error HTTP/1.1 500

The application exposes Prometheus metrics through:

    /metrics

---

## 11. Prometheus Configuration

Prometheus is responsible for collecting application metrics.

The application exposes the following metric:

    app_http_requests_total

This metric records HTTP request activity.

The metric contains labels such as:

    endpoint
    instance
    job
    method
    status

Example metric series:

    {endpoint="/", instance="app:5000", job="observability-app", method="GET", status="200"}

    {endpoint="/api/data", instance="app:5000", job="observability-app", method="GET", status="200"}

    {endpoint="/api/error", instance="app:5000", job="observability-app", method="GET", status="500"}

    {endpoint="/health", instance="app:5000", job="observability-app", method="GET", status="200"}

### Prometheus Query

Basic metric query:

    app_http_requests_total

Request-rate query:

    rate(app_http_requests_total[5m])

The rate query is used to visualize HTTP request activity over time.

---

## 12. Loki Configuration

Loki is used for centralized log storage.

Application logs generated inside the Docker environment are collected by Promtail and forwarded to Loki.

Grafana uses Loki as a log data source.

The application can be selected using the LogQL query:

    {service_name="observability-app"}

This query displays logs generated by the application.

---

## 13. Promtail Configuration

Promtail acts as the log collection agent.

It reads Docker container logs and sends them to Loki.

The configuration collects logs from Docker containers and attaches labels such as:

    container
    filename
    job
    service_name
    stream

The following label was used to identify the application:

    service_name="observability-app"

The resulting LogQL selector is:

    {service_name="observability-app"}

---

## 14. Grafana Configuration

Grafana is used as the main visualization and monitoring interface.

Grafana runs on:

    http://localhost:3001

The configured data sources include:

- Prometheus
- Loki
- Jaeger

Grafana was used to verify that the observability data was successfully received.

---

## 15. Grafana Dashboard

A dashboard named:

    Observability Dashboard

was created.

The dashboard contains monitoring panels for:

### Application Logs

Data source:

    Loki

Query:

    {service_name="observability-app"}

This panel displays application logs collected through Promtail.

### HTTP Requests

Data source:

    Prometheus

Query:

    rate(app_http_requests_total[5m])

This panel displays HTTP request activity over time.

---

## 16. Log Monitoring and Verification

Loki was successfully queried through Grafana Explore.

The application produced informational logs such as:

    Home endpoint requested

    Home endpoint completed status=200

    Data API request started

    Data API request completed status=200 duration=0.2603s

The application also produced an intentional error:

    ERROR observability-app Intentional test error generated

The corresponding HTTP request was:

    GET /api/error HTTP/1.1 500

This demonstrates that both normal application activity and error activity can be monitored.

---

## 17. Prometheus Verification

Prometheus successfully discovered the Flask application's metrics.

The following HTTP request metric series were observed:

    endpoint="/"
    status="200"

    endpoint="/api/data"
    status="200"

    endpoint="/api/error"
    status="500"

    endpoint="/health"
    status="200"

This confirms that Prometheus is successfully collecting application-level HTTP metrics.

---

## 18. Jaeger Configuration

Jaeger provides distributed tracing capabilities.

Jaeger is configured using the Jaeger All-in-One image.

Jaeger UI:

    http://localhost:16686

OTLP ports:

    4317
    4318

Jaeger is included in the observability architecture to provide request tracing capabilities.

---

## 19. Service Ports

| Service | Port |
|---|---:|
| Flask Application | 5000 |
| Grafana | 3001 |
| Prometheus | 9090 |
| Loki | 3100 |
| Jaeger UI | 16686 |
| Jaeger OTLP | 4317 |
| Jaeger OTLP HTTP | 4318 |

---

## 20. Testing Procedure

The following testing procedure was used.

### Step 1: Start the Stack

Command:

    docker compose up -d

### Step 2: Verify Containers

Command:

    docker compose ps

All major services were verified to be running.

### Step 3: Test Application

The following endpoints were accessed:

    /
    /health
    /api/data
    /api/error
    /metrics

### Step 4: Verify Prometheus

Prometheus was opened at:

    http://localhost:9090

The metric:

    app_http_requests_total

was queried successfully.

### Step 5: Verify Loki

Grafana Explore was opened with Loki selected.

The query:

    {service_name="observability-app"}

was executed successfully.

### Step 6: Verify Error Logs

The intentional error endpoint was triggered and the following was observed:

    GET /api/error HTTP/1.1 500

and:

    ERROR observability-app Intentional test error generated

### Step 7: Verify Grafana Dashboard

The HTTP Requests and Application Logs panels were verified in Grafana.

### Step 8: Restart Verification

The complete stack was stopped and started again using:

    docker compose down

    docker compose up -d

The services successfully started again.

---

## 21. Final Docker Verification

The final `docker compose ps` output confirmed that the following services were running:

    observability-app
    observability-grafana
    observability-jaeger
    observability-loki
    observability-prometheus
    observability-promtail

The services were successfully running after restarting the complete stack.

---

## 22. Screenshots / Evidence

Screenshots were captured during the implementation and verification process.

The screenshots directory contains evidence of the following activities:

### Screenshot 01
Grafana interface / initial setup.

### Screenshot 02
Grafana data source configuration.

### Screenshot 03
Loki data source verification.

### Screenshot 04
Loki label browser showing available labels.

### Screenshot 05
Loki error log showing the intentional application error.

### Screenshot 06
Loki informational application logs.

### Screenshot 07
Grafana Explore view showing application logs.

### Screenshot 08
Grafana HTTP Requests panel using Prometheus.

### Screenshot 09
Prometheus metric results showing HTTP request series.

### Screenshot 10
Final Grafana Observability Dashboard.

### Screenshot 11
Final Docker Compose service status.

The screenshots serve as implementation and verification evidence.

---

## 23. Results

The implementation successfully achieved the intended observability objectives.

### Metrics

Prometheus successfully collected application HTTP metrics.

The metric:

    app_http_requests_total

was successfully queried.

### Logs

Promtail successfully collected Docker application logs.

Loki successfully stored and returned the logs.

Grafana successfully displayed the logs.

### Errors

The intentional `/api/error` endpoint generated an HTTP 500 response.

The corresponding application error was successfully visible in Loki.

### Visualization

Grafana successfully displayed:

- Application logs
- HTTP request metrics
- Prometheus data
- Loki data

### Containers

All required Docker Compose services successfully started and remained operational.

---

## 24. Troubleshooting

### Problem 1: Grafana Data Source

Initially, data source configuration was verified through Grafana.

After configuration, the data source successfully returned data.

### Problem 2: Loki Query Returned No Logs

The correct application label was identified using the Loki label browser.

The working selector was:

    {service_name="observability-app"}

After running the query, application logs were successfully displayed.

### Problem 3: Prometheus Query

The Prometheus metric browser showed the application metric:

    app_http_requests_total

The metric returned multiple endpoint and status combinations.

### Problem 4: Dashboard Persistence

The Grafana dashboard was exported as JSON and saved as a project dashboard file so that the dashboard configuration could be preserved outside the Grafana container.

### Problem 5: Container Restart Verification

The complete stack was tested using:

    docker compose down

followed by:

    docker compose up -d

The services successfully restarted.

---

## 25. Key Observations

The project demonstrated the following important observations:

1. Application metrics can be collected independently from application logs.
2. Prometheus provides structured numerical monitoring data.
3. Loki provides centralized log searching.
4. Promtail acts as the bridge between Docker logs and Loki.
5. Grafana provides a centralized interface for monitoring.
6. HTTP 500 errors can be detected through both metrics and logs.
7. Docker Compose simplifies deployment of the complete observability stack.
8. Persistent volumes allow monitoring data to survive container recreation.
9. Labels make log filtering easier in Loki.
10. Rate calculations provide useful time-series information from counter metrics.

---

## 26. Advantages

The implemented system provides several advantages:

- Centralized monitoring.
- Centralized log management.
- Application error visibility.
- HTTP request monitoring.
- Real-time visualization.
- Containerized deployment.
- Easy local development.
- Open-source technology stack.
- Separate metrics, logs, and tracing components.
- Easy service management using Docker Compose.

---

## 27. Limitations

The current implementation is primarily designed for local development and demonstration.

Some production-level features are not included, such as:

- Production authentication.
- HTTPS/TLS.
- Advanced alerting.
- High availability.
- Cloud deployment.
- Long-term production log retention.
- Advanced distributed tracing dashboards.
- Production-grade secret management.

---

## 28. Future Enhancements

The following improvements can be added in future versions:

1. Add Grafana alert rules.
2. Monitor CPU and memory usage.
3. Add Docker container metrics.
4. Add application latency metrics.
5. Create HTTP error-rate panels.
6. Integrate more detailed Jaeger tracing.
7. Add service-level indicators.
8. Add service-level objectives.
9. Configure email or messaging alerts.
10. Add CI/CD automation.
11. Deploy the system to AWS.
12. Implement HTTPS and authentication.
13. Add production-grade persistent storage.
14. Add automated health checks.

---

## 29. Learning Outcomes

Through this project, the following practical concepts were demonstrated:

- Docker containerization.
- Docker Compose.
- Flask application monitoring.
- Prometheus metrics.
- PromQL queries.
- Loki log aggregation.
- LogQL queries.
- Promtail log collection.
- Grafana dashboards.
- Grafana data sources.
- Jaeger distributed tracing.
- Docker networking.
- Persistent Docker volumes.
- HTTP monitoring.
- Error monitoring.
- Application troubleshooting.
- Observability architecture.

---

## 30. Conclusion

The Complete Observability System successfully demonstrates an end-to-end observability architecture for a containerized Flask application.

Prometheus was used to collect application metrics, while Promtail collected Docker logs and forwarded them to Loki. Grafana provided a centralized interface for querying and visualizing metrics and logs. Jaeger was included to provide distributed tracing capabilities.

The system successfully detected normal HTTP requests, health checks, API activity, and intentional HTTP 500 errors.

The final implementation demonstrates how Metrics, Logs, and Traces can be combined to provide better visibility into application behavior and simplify monitoring and troubleshooting.

Overall, the project provides practical hands-on experience with modern DevOps observability tools and demonstrates how multiple open-source components can be integrated into a single monitoring platform.

---

## 31. Final Project Status

| Component | Status |
|---|---|
| Flask Application | Completed |
| Docker Containerization | Completed |
| Docker Compose | Completed |
| Prometheus Metrics | Completed |
| Loki Logging | Completed |
| Promtail Log Collection | Completed |
| Grafana Visualization | Completed |
| Grafana Dashboard | Completed |
| Jaeger Service | Completed |
| Error Monitoring | Completed |
| Testing | Completed |
| Screenshot Evidence | Completed |
| Documentation | Completed |

---

## 32. Final Summary

The project successfully implements:

    Application
         ↓
    Metrics → Prometheus
         ↓
    Grafana

    Application
         ↓
    Docker Logs → Promtail → Loki
         ↓
    Grafana

    Application
         ↓
    Traces → Jaeger

This completes the implementation of a local, containerized observability system based on:

**Prometheus + Grafana + Loki + Promtail + Jaeger + Docker Compose**