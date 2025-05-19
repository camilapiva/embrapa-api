from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging import logger
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"{settings.project_name} started in {settings.environment} mode.")
    yield
    logger.info(f"{settings.project_name} is shutting down.")

app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="REST API to retrieve viticulture data from Embrapa.",
    lifespan=lifespan
)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.project_name}"}
