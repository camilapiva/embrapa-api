from fastapi import APIRouter, Query, Depends, HTTPException
from app.services.exportation import fetch_exportation_data, EXPORT_TYPE_TO_SUBOPT
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger
from app.models.exportation_types import ExportTypeEnum

logger = setup_logger(__name__)
router = APIRouter(prefix="/exportation", tags=["Exportation"]) 

@router.get("/", dependencies=[Depends(get_current_user)])
def get_exportation_data(
    year: int = Query(..., ge=1970, le=2023),
    export_type: ExportTypeEnum = Query(..., alias="type")
):
    """
    Returns the exportation data for the specified year and grape type.
    Example: /exportation/?year=2022&type=subopt_01
    """
    subopt_code = EXPORT_TYPE_TO_SUBOPT.get(export_type)
    if not subopt_code:
        logger.warning(f"Invalid export type: {export_type}")
        raise HTTPException(status_code=400, detail="Invalid export type.")

    data = fetch_exportation_data(year, subopt_code)

    if not data:
        logger.warning(f"No exportation data found for year {year} and type {export_type}")
        raise HTTPException(status_code=503, detail="Unable to fetch exportation data from Embrapa or fallback.")
    return data
