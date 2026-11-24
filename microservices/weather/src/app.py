import time
from fastapi import FastAPI, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Weather Microservice")

WEATHER_FETCHES = Counter("weather_fetches_total", "Total forecast fetches", ["status"])
WEATHER_FETCH_DURATION = Histogram("weather_fetch_duration_seconds", "Weather fetch duration in seconds")

@app.get("/")
def root():
    return {"service": "weather", "status": "running", "port": 8002}

@app.get("/health")
def health():
    return {"status": "UP", "service": "weather"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/api/weather/forecast")
def forecast(village: str = "Belgaum"):
    start = time.time()
    WEATHER_FETCHES.labels(status="success").inc()
    duration = time.time() - start
    WEATHER_FETCH_DURATION.observe(duration)
    return {
        "location": village,
        "temperature_c": 33.5,
        "relative_humidity": 62,
        "condition": "Sunny / Heatwave Alert"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
