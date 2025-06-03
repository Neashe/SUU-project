from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from random import randint
from time import sleep
import httpx
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

exporter = OTLPMetricExporter(endpoint="http://localhost:4317", insecure=True)
reader = PeriodicExportingMetricReader(exporter)
resource = Resource.create({"service.name": "frontend-gateway"})
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)

meter = metrics.get_meter(__name__)
request_counter = meter.create_counter(
    name="gateway_requests_total",
    unit="1",
    description="Total number of requests to Frontend Gateway",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or ["http://localhost:3000"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example: Aggregate jokes with their ratings and image URLs
@app.get("/jokes/full")
async def get_full_jokes():
    request_counter.add(1, {"endpoint": "/jokes/full"})
    async with httpx.AsyncClient() as client:
        jokes_resp = await client.get("http://localhost:8001/jokes")
        jokes = jokes_resp.json().get("jokes", [])
        for joke in jokes:
            rating_resp = await client.get(f"http://localhost:8002/rating/{joke['id']}")
            rating = rating_resp.json().get("average_rating", 0)
            joke["average_rating"] = rating
            if joke.get("meme"):
                joke["image_url"] = f"http://localhost:8005/media/{joke['meme']}"
            else:
                joke["image_url"] = None
    return {"jokes": jokes}

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/stats/record")
async def record_stats(data: dict):
    joke_id = data.get("joke_id")
    rating = data.get("rating")
    async with httpx.AsyncClient() as client:
        # Always record a view
        await client.post("http://localhost:8004/stats/view", json={"joke_id": joke_id})
        # Send rating to Rating Service if provided
        if rating is not None:
            await client.post(f"http://localhost:8002/rate/{joke_id}", params={"rating": rating})
    return {"status": "ok"}

@app.get("/ranking")
async def get_ranking():
    async with httpx.AsyncClient() as client:
        resp = await client.get("http://localhost:8003/ranking")
        return resp.json()
