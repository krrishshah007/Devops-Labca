from fastapi import FastAPI, Response
from pydantic import BaseModel
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="Auth Microservice")

REGISTRATIONS_TOTAL = Counter("auth_registrations_total", "Total user registrations")
LOGINS_TOTAL = Counter("auth_logins_total", "Total user logins")

class AuthRequest(BaseModel):
    username: str
    password: str

@app.get("/")
def root():
    return {"service": "auth", "status": "running", "port": 8001}

@app.get("/health")
def health():
    return {"status": "UP", "service": "auth"}

@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/api/auth/register")
def register(req: AuthRequest):
    REGISTRATIONS_TOTAL.inc()
    return {"status": "success", "message": f"User {req.username} registered"}

@app.post("/api/auth/login")
def login(req: AuthRequest):
    LOGINS_TOTAL.inc()
    return {"status": "success", "token": "jwt_token_sample", "username": req.username}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
