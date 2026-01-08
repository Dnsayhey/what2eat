from fastapi import FastAPI

from src.core.config import settings
from src.core.database import create_db_and_tables


app = FastAPI()


@app.get("/")
async def index():
    return {
        "message": f"Hello from the {settings.app_name}!"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/init-db")
async def init_db():
    await create_db_and_tables()
    return {"status": "ok"}
