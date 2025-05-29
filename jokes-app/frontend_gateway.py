from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from random import randint
from time import sleep
import httpx
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
    name="gateway_requests_total",
    unit="1",
    description="Total number of requests to Frontend Gateway",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

# Example: Aggregate jokes with their ratings and image URLs
@app.get("/jokes/full")
async def get_full_jokes():
    request_counter.add(1, {"endpoint": "/jokes/full"})
    sleep(randint(1, 2))
    async with httpx.AsyncClient() as client:
        jokes_resp = await client.get("http://localhost:8001/jokes")
        jokes = jokes_resp.json().get("jokes", [])
        for joke in jokes:
            rating_resp = await client.get(f"http://localhost:8002/rating/{joke['id']}")
            rating = rating_resp.json().get("average_rating", 0)
            joke["average_rating"] = rating
            # Optionally, add image URL if you have mapping
            joke["image_url"] = f"/media/{joke['id']}.png"
    return {"jokes": jokes}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}
