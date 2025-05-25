from fastapi import APIRouter, Query, Depends, HTTPException
from app.scraping.exportation import fetch_exportation_data
from app.core.auth import get_current_user
from app.logging.logger import setup_logger

logger = setup_logger(__name__)
router = APIRouter(prefix="/exportation", tags=["Exportation"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_exportation_data(
    year: int = Query(..., ge=1970, le=2023),
    export_type: str = Query(..., pattern="^subopt_0[1-4]$")
):
    """
    Returns the exportation data for the specified year and grape type.
    Example: /exportation/?year=2022&type=subopt_01
    """
    data = fetch_exportation_data(year, export_type)
    if not data:
        logger.warning(f"No exportation data found for year {year} and type {export_type}")
        raise HTTPException(status_code=503, detail="Unable to fetch exportation data from Embrapa or fallback.")
    return data
