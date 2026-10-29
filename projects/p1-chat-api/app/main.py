from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.core.config import settings
from app.core.log import setup_logging

setup_logging()

app = FastAPI(title=settings.app_name, version=settings.version)

app.include_router(chat_router)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status":"ok","version":settings.version}