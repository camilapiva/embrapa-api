from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Literal
from app.core.auth import get_current_user
from app.scraping.processing import fetch_processing_data
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/processing", tags=["Processing"])

GrapeType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

@router.get("/", dependencies=[Depends(get_current_user)])
def get_processing_data(
    year: int = Query(..., ge=1970, le=2023),
    grape_type: GrapeType = Query(..., alias="type")
):
    """
    Returns the processing data for the specified year and grape type.
    Example: /processing/?year=2022&type=subopt_01
    """
    data = fetch_processing_data(year, grape_type)
    if not data:
        logger.warning(f"No processing data found for year {year} and type {grape_type}")
        raise HTTPException(status_code=503,detail="Unable to fetch processing data from Embrapa or fallback.")
    return data
