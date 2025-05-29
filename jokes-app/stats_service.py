from fastapi import FastAPI
from random import randint
from datetime import datetime
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    name="stats_requests_total",
    unit="1",
    description="Total number of requests to Stats Service",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

# In-memory stats storage for demonstration
stats = {
    "ratings_per_day": {},
    "views_per_day": {},
}

def today():
    return datetime.now().strftime("%Y-%m-%d")

@app.post("/stats/rating")
def add_rating_stat(joke_id: int = None):
    request_counter.add(1, {"endpoint": "/stats/rating"})
    d = today()
    stats["ratings_per_day"][d] = stats["ratings_per_day"].get(d, 0) + 1
    return {"date": d, "ratings": stats["ratings_per_day"][d]}

@app.post("/stats/view")
def add_view_stat(joke_id: int = None):
    request_counter.add(1, {"endpoint": "/stats/view"})
    d = today()
    stats["views_per_day"][d] = stats["views_per_day"].get(d, 0) + 1
    return {"date": d, "views": stats["views_per_day"][d]}

@app.get("/stats")
def get_stats():
    request_counter.add(1, {"endpoint": "/stats"})
    return stats
