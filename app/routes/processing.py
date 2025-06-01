from fastapi import APIRouter, Query, HTTPException, Depends
from app.models.processing_types import GrapeTypeEnum
from app.auth.dependencies import get_current_user
from app.services.processing import fetch_processing_data, GRAPE_TYPE_TO_SUBOPT
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/processing", tags=["Processing"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_processing_data(
    year: int = Query(..., ge=1970, le=2023),
    grape_type: GrapeTypeEnum = Query(..., alias="type")
):
    """
    Returns the processing data for the specified year and grape type.
    Example: /processing/?year=2022&type=Viníferas
    """
    subopt_code = GRAPE_TYPE_TO_SUBOPT.get(grape_type)
    if not subopt_code:
        logger.warning(f"Invalid grape type: {grape_type}")
        raise HTTPException(status_code=400, detail="Invalid grape type.")

    data = fetch_processing_data(year, subopt_code)
    if not data:
        logger.warning(f"No processing data found for year {year} and type {grape_type}")
        raise HTTPException(status_code=503, detail="Unable to fetch processing data from Embrapa or fallback.")
    return data
