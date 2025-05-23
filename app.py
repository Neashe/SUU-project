from fastapi import FastAPI
from random import randint
from time import sleep

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
    name="app_requests_total",
    unit="1",
    description="Total number of requests",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

@app.get("/hello")
def read_root():
    request_counter.add(1, {"endpoint": "/hello"})
    sleep(randint(1, 3))
    return {"message": "Hello, FastAPI!"}
