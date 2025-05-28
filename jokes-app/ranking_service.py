from fastapi import FastAPI
from random import randint
from time import sleep
from typing import List

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    name="ranking_requests_total",
    unit="1",
    description="Total number of requests to Ranking Service",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

# Mocked data for demonstration
mock_jokes = [
    {"id": 1, "joke": "Why did the chicken cross the road? To get to the other side!", "average_rating": 4.5},
    {"id": 2, "joke": "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'", "average_rating": 3.8},
]

@app.get("/ranking")
def get_ranking(limit: int = 10):
    request_counter.add(1, {"endpoint": "/ranking"})
    sleep(randint(1, 2))
    # In a real implementation, fetch ratings from Rating Service and sort
    sorted_jokes = sorted(mock_jokes, key=lambda x: x["average_rating"], reverse=True)
    return {"ranking": sorted_jokes[:limit]}
