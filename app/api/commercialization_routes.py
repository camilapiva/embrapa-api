from fastapi import APIRouter, Query, Depends, HTTPException
from app.scraping.commercialization import fetch_commercialization_data
from app.core.auth import get_current_user
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/commercialization", tags=["Commercialization"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_commercialization_data(year: int = Query(..., ge=1970, le=2023)):
    """
    Returns the commercialization data for the specified year.
    Example: /commercialization/?year=2022
    """
    data = fetch_commercialization_data(year)
    if not data:
        logger.warning(f"No commercialization data found for year {year}")
        raise HTTPException(status_code=503, detail="Unable to fetch commercialization data or fallback.")
    return data
