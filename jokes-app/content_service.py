from fastapi import FastAPI
from random import randint

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
    name="content_requests_total",
    unit="1",
    description="Total number of requests to Content Service",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

jokes = [
    {"id": 1, "joke": "Why did the chicken cross the road? To get to the other side!", "meme": "Asterix_Obelix.jpg"},
    {"id": 2, "joke": "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'", "meme": None},
]

@app.get("/jokes")
def get_jokes():
    request_counter.add(1, {"endpoint": "/jokes"})
    return {"jokes": jokes}

@app.get("/jokes/random")
def get_random_joke():
    request_counter.add(1, {"endpoint": "/jokes/random"})
    joke = jokes[randint(0, len(jokes)-1)]
    return joke

@app.get("/jokes/{joke_id}")
def get_joke_by_id(joke_id: int):
    request_counter.add(1, {"endpoint": "/jokes/{joke_id}"})
    for joke in jokes:
        if joke["id"] == joke_id:
            return joke
    return {"error": "Joke not found"}
