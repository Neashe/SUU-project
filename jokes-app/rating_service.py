from fastapi import FastAPI
from random import randint
from time import sleep

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
resource = Resource.create({"service.name": "rating-service"})
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    name="rating_requests_total",
    unit="1",
    description="Total number of requests to Rating Service",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

ratings = {}  # {joke_id: [ratings]}

@app.post("/rate/{joke_id}")
def rate_joke(joke_id: int, rating: int):
    request_counter.add(1, {"endpoint": "/rate"})
    if joke_id not in ratings:
        ratings[joke_id] = []
    ratings[joke_id].append(rating)
    return {"joke_id": joke_id, "ratings": ratings[joke_id]}

@app.get("/rating/{joke_id}")
def get_rating(joke_id: int):
    request_counter.add(1, {"endpoint": "/rating"})
    joke_ratings = ratings.get(joke_id, [])
    avg = sum(joke_ratings) / len(joke_ratings) if joke_ratings else 0
    return {"joke_id": joke_id, "average_rating": avg, "ratings": joke_ratings}

@app.get("/ratings")
def get_all_ratings():
    request_counter.add(1, {"endpoint": "/ratings"})
    all_ratings = {}
    for joke_id, joke_ratings in ratings.items():
        avg = sum(joke_ratings) / len(joke_ratings) if joke_ratings else 0
        all_ratings[joke_id] = {
            "average_rating": avg,
            "ratings": joke_ratings
        }
    return {"ratings": all_ratings}
