from fastapi import APIRouter, Query, HTTPException, Depends
from app.schemas.schema import ProductionResponse
from app.services.extractions.production import ProductionExtractor, fetch_production_data
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/production", tags=["Production"])


@router.get("/", dependencies=[Depends(get_current_user)], response_model=ProductionResponse)
def get_production_data(year: int = Query(..., ge=1970, le=2023)) -> ProductionResponse:
    """
    Returns the production data for the specified year.
    Example: /production/?year=2022
    """
    extractor = ProductionExtractor()
    data = extractor.fetch_data(year)
    if not data:
        logger.warning(f"Unable to fetch production data from Embrapa or fallback.")
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch production data from Embrapa or fallback.",
        )
    return data
