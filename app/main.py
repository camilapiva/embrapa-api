from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging.logger import setup_logger
from app.core.config import settings

from app.routes.auth import router as auth_router
from app.routes.protected import router as protected_router
from app.routes.production import router as production_router
from app.routes.processing import router as processing_router
from app.routes.exportation import router as exportation_router
from app.routes.importation import router as importation_router
from app.routes.commercialization import router as commercialization_router
from app.routes.predict import router as predict_router

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
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(protected_router)
app.include_router(production_router)
app.include_router(processing_router)
app.include_router(exportation_router)
app.include_router(importation_router)
app.include_router(commercialization_router)
app.include_router(predict_router)


@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": f"Welcome to {settings.project_name}"}
