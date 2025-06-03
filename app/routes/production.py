from fastapi import APIRouter, Query, HTTPException, Depends
from app.services.production import fetch_production_data
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/production", tags=["Production"])


@router.get("/", dependencies=[Depends(get_current_user)])
def get_production_data(year: int = Query(..., ge=1970, le=2023)):
    """
    Returns the production data for the specified year.
    Example: /production/?year=2022
    """
    data = fetch_production_data(year)
    if not data:
        logger.warning(f"No production data found for year {year}")
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch production data from Embrapa or fallback.",
        )
    return data
