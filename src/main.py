from fastapi import FastAPI

from src.core.config import settings
from src.auth.route import router as auth_router
from src.dishes.route import router as dishes_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(dishes_router)


@app.get("/")
async def index():
    return {"message": f"Hello from the {settings.app_name}!"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}

