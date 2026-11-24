import os
import time
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
import requests
from prometheus_client import Counter, Gauge, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Gateway Microservice")

# Metrics
GATEWAY_REQUESTS = Counter(
    "gateway_requests_total",
    "Total requests through API gateway",
    ["method", "route", "status"]
)
INVENTORY_ACTIONS = Counter(
    "inventory_actions_total",
    "Inventory modification actions recorded",
    ["action", "category", "source"]
)
NEWS_REQUESTS = Counter(
    "news_generation_requests_total",
    "Gemini news generation requests",
    ["result"]
)
CIRCUIT_BREAKER_STATE = Gauge(
    "circuit_breaker_state",
    "Circuit breaker state: 0=closed, 1=open, 2=half-open",
    ["service"]
)
FALLBACK_TOTAL = Counter(
    "fallback_total",
    "Fallback responses served",
    ["service"]
)

CIRCUIT_BREAKER_STATE.labels(service="weather").set(0)

@app.middleware("http")
async def track_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    route = request.url.path
    if route != "/metrics":
        GATEWAY_REQUESTS.labels(
            method=request.method,
            route=route,
            status=str(response.status_code)
        ).inc()
    return response

@app.get("/")
def root():
    return {"service": "gateway", "status": "running", "port": 8000}

@app.get("/health")
def health():
    return {"status": "UP", "service": "gateway"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/metrics/inventory")
def record_inventory_event(action: str = "add", category: str = "general", source: str = "demo"):
    INVENTORY_ACTIONS.labels(action=action, category=category, source=source).inc()
    return {"status": "recorded", "action": action, "category": category, "source": source}

@app.get("/api/advisory")
def get_advisory():
    advisory_url = os.getenv("ADVISORY_URL", "http://advisory:8003")
    try:
        res = requests.get(f"{advisory_url}/api/v1/advisory", timeout=3)
        return res.json()
    except Exception as e:
        FALLBACK_TOTAL.labels(service="advisory").inc()
        return {"status": "fallback", "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
