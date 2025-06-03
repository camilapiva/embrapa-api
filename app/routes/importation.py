from fastapi import APIRouter, Query, Depends, HTTPException
from app.schemas.schema import ImportationResponse
from app.services.extractions.importation import fetch_importation_data, IMPORT_TYPE_TO_SUBOPT
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger
from app.models.importation_types import ImportTypeEnum

logger = setup_logger(__name__)
router = APIRouter(prefix="/importation", tags=["Importation"])


@router.get("/", dependencies=[Depends(get_current_user)], response_model=ImportationResponse)
def get_importation_data(
    year: int = Query(..., ge=1970, le=2023),
    import_type: ImportTypeEnum = Query(..., alias="type"),
) -> ImportationResponse:
    """
    Returns the importation data for the specified year and grape type.
    Example: /importation/?year=2022&type=subopt_01
    """
    subopt_code = IMPORT_TYPE_TO_SUBOPT.get(import_type)
    if not subopt_code:
        logger.warning(f"Invalid import type: {import_type}")
        raise HTTPException(status_code=400, detail="Invalid import type.")

    data = fetch_importation_data(year, subopt_code)

    if not data:
        logger.warning(
            f"No importation data found for year {year} and type {import_type}"
        )
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch importation data from Embrapa or fallback.",
        )
    return data
