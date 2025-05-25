from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging.logger import setup_logger
from app.core.config import settings

from app.api.auth_routes import router as auth_router
from app.api.protected_routes import router as protected_router
from app.api.production_routes import router as production_router
from app.api.processing_routes import router as processing_router
from app.api.exportation_routes import router as exportation_router
from app.api.importation_routes import router as importation_router
from app.api.commercialization_routes import router as commercialization_router

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

app.include_router(auth_router)
app.include_router(protected_router)
app.include_router(production_router)
app.include_router(processing_router)
app.include_router(exportation_router)
app.include_router(importation_router)
app.include_router(commercialization_router)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.project_name}"}
