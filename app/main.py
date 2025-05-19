from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.logging import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("✅ API Embrapa started successfully.")
    yield
    logger.info("🛑 API Embrapa is shutting down.")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to Embrapa API"}
