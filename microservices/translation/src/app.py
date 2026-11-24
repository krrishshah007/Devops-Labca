from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Translation Microservice")

TRANSLATIONS_TOTAL = Counter(
    "translations_total",
    "Number of translations grouped by language",
    ["language"]
)

class TranslationRequest(BaseModel):
    text: str
    target_language: str = "hi"

@app.get("/")
def root():
    return {"service": "translation", "status": "running", "port": 8004}

@app.get("/health")
def health():
    return {"status": "UP", "service": "translation"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/translation/translate")
def translate(req: TranslationRequest):
    TRANSLATIONS_TOTAL.labels(language=req.target_language).inc()
    return {
        "status": "success",
        "original": req.text,
        "translated": f"[{req.target_language.upper()}] {req.text}",
        "language": req.target_language
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
