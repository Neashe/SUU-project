from fastapi import FastAPI
from random import randint
from time import sleep

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
    {"id": 1, "joke": "Why did the chicken cross the road? To get to the other side!"},
    {"id": 2, "joke": "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.'"},
]

@app.get("/jokes")
def get_jokes():
    request_counter.add(1, {"endpoint": "/jokes"})
    sleep(randint(1, 2))
    return {"jokes": jokes}
