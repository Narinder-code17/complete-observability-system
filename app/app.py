import logging
import random
import time

from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# --------------------------------------------------
# Logging Configuration
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger("observability-app")


# --------------------------------------------------
# Flask Application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Prometheus Metrics
# --------------------------------------------------

REQUEST_COUNT = Counter(
    "app_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "app_http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)


# --------------------------------------------------
# OpenTelemetry / Jaeger Tracing
# --------------------------------------------------

resource = Resource.create(
    {
        "service.name": "observability-demo-app",
        "service.version": "1.0.0",
        "deployment.environment": "docker-compose",
    }
)

tracer_provider = TracerProvider(resource=resource)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4317",
    insecure=True,
)

tracer_provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

trace.set_tracer_provider(tracer_provider)

tracer = trace.get_tracer(__name__)

FlaskInstrumentor().instrument_app(app)


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.route("/")
def home():
    start_time = time.time()

    logger.info("Home endpoint requested")

    response = jsonify(
        {
            "application": "Complete Observability Demo",
            "version": "1.0.0",
            "status": "running",
        }
    )

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/",
        status=response.status_code,
    ).inc()

    REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/",
    ).observe(duration)

    logger.info(
        "Home endpoint completed status=%s duration=%.4fs",
        response.status_code,
        duration,
    )

    return response


@app.route("/health")
def health():
    logger.info("Health check requested")

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/health",
        status=200,
    ).inc()

    return jsonify({"status": "healthy"})


@app.route("/api/data")
def get_data():
    start_time = time.time()

    logger.info("Data API request started")

    time.sleep(random.uniform(0.05, 0.3))

    data = {
        "service": "observability-demo-app",
        "message": "Observability data generated successfully",
        "items": [1, 2, 3, 4, 5],
    }

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/api/data",
        status=200,
    ).inc()

    REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/api/data",
    ).observe(duration)

    logger.info(
        "Data API request completed status=200 duration=%.4fs",
        duration,
    )

    return jsonify(data)


@app.route("/api/error")
def generate_error():
    logger.error("Intentional test error generated")

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/api/error",
        status=500,
    ).inc()

    return jsonify(
        {
            "error": "Intentional test error",
            "message": "This endpoint is used to demonstrate observability.",
        }
    ), 500


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {
        "Content-Type": CONTENT_TYPE_LATEST
    }


# --------------------------------------------------
# Application Startup
# --------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Complete Observability Demo")

    app.run(
        host="0.0.0.0",
        port=5000,
    )