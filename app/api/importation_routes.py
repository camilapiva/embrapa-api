from fastapi import APIRouter, Query, Depends, HTTPException
from app.scraping.importation import fetch_importation_data
from app.core.auth import get_current_user
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/importation", tags=["Importation"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_importation_data(
    year: int = Query(..., ge=1970, le=2023),
    import_type: str = Query(..., pattern="^subopt_0[1-5]$")
):
    """
    Returns the importation data for the specified year and grape type.
    Example: /importation/?year=2022&type=subopt_01
    """
    data = fetch_importation_data(year, import_type)
    if not data:
        logger.warning(f"No importation data found for year {year} and type {import_type}")
        raise HTTPException(status_code=503, detail="Unable to fetch importation data from Embrapa or fallback.")
    return data
