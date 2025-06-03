from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.schema import CommercializationResponse
from app.services.extractions.commercialization import fetch_commercialization_data
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger
from app.services.queryDB.commercialization import fetch_commercializations_from_db

logger = setup_logger(__name__)
router = APIRouter(prefix="/commercialization", tags=["Commercialization"])


@router.get("/", dependencies=[Depends(get_current_user)], response_model=CommercializationResponse)
async def get_commercialization_data(year: int = Query(..., ge=1970, le=2023)) -> CommercializationResponse:
    """
    Returns the commercialization data for the specified year.
    Example: /commercialization/?year=2022
    """
    data = fetch_commercialization_data(year)
    if not data:
        logger.warning(f"Failed to fetch commercialization data from both Embrapa and database fallback.")
        
    return data
