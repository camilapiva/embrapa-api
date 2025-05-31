from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging.logger import setup_logger
from app.core.config import settings

from app.routes.auth import router as auth
from app.routes.protected import router as protected
from app.routes.production import router as production
from app.routes.processing import router as processing
from app.routes.exportation import router as exportation
from app.routes.importation import router as importation
from app.routes.commercialization import router as commercialization

logger = setup_logger(__name__)

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

app.include_router(auth)
app.include_router(protected)
app.include_router(production)
app.include_router(processing)
app.include_router(exportation)
app.include_router(importation)
app.include_router(commercialization)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.project_name}"}
