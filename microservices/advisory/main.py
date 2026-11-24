import time
from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Advisory Microservice")

ADVISORY_DECISIONS = Counter(
    "advisory_decisions_total",
    "Total advisory decisions computed",
    ["decision"]
)
ADVISORY_DURATION = Histogram(
    "advisory_duration_seconds",
    "Time taken to compute advisory decisions"
)

class AdvisoryRequest(BaseModel):
    crop: str = "Sugarcane"
    soil_type: str = "Loamy"
    temperature: float = 34.0
    humidity: float = 55.0

@app.get("/")
def root():
    return {"service": "advisory", "status": "running", "port": 8003}

@app.get("/health")
def health():
    return {"status": "UP", "service": "advisory"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/v1/advisory")
def default_advisory():
    return compute_advisory(AdvisoryRequest())

@app.post("/api/v1/advisory/generate")
def compute_advisory(req: AdvisoryRequest):
    start = time.time()
    if req.temperature > 35.0:
        decision = "IRRIGATE_HIGH"
        msg = "High heat anomaly detected. Immediate irrigation recommended."
    elif req.temperature > 30.0:
        decision = "IRRIGATE_MODERATE"
        msg = "Standard irrigation cycle recommended."
    else:
        decision = "OPTIMAL"
        msg = "Soil moisture within acceptable threshold."
    
    ADVISORY_DECISIONS.labels(decision=decision).inc()
    ADVISORY_DURATION.observe(time.time() - start)
    return {
        "status": "success",
        "decision": decision,
        "recommendation": msg,
        "crop": req.crop,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
