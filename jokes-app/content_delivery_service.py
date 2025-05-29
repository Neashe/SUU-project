from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from random import randint
from time import sleep
import os
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
    name="delivery_requests_total",
    unit="1",
    description="Total number of requests to Content Delivery Service",
)

app = FastAPI()
FastAPIInstrumentor().instrument_app(app)

MEDIA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
os.makedirs(MEDIA_DIR, exist_ok=True)

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    request_counter.add(1, {"endpoint": "/upload"})
    sleep(randint(1, 2))
    file_path = os.path.join(MEDIA_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    return {"filename": file.filename, "url": f"/media/{file.filename}"}

@app.get("/media/{filename}")
def get_file(filename: str):
    request_counter.add(1, {"endpoint": "/media"})
    sleep(randint(1, 2))
    file_path = os.path.join(MEDIA_DIR, filename)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path)
