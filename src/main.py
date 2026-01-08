from fastapi import FastAPI

from src.core.config import settings


app = FastAPI()


@app.get("/")
def index():
    return {
        "message": f"Hello from the {settings.app_name}!"
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}