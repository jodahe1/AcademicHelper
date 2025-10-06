from fastapi import FastAPI
from database import init_db

app = FastAPI(title="Academic Helper API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup() -> None:
    # Create tables on startup (idempotent)
    init_db()
