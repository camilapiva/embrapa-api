from fastapi import APIRouter, Query, Depends, HTTPException
from app.scraping.importation import fetch_importation_data
from app.core.auth import get_current_user

router = APIRouter(prefix="/importation", tags=["Importation"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_importation_data(
    year: int = Query(..., ge=1970, le=2023),
    import_type: str = Query(..., pattern="^subopt_0[1-5]$")
):
    data = fetch_importation_data(year, import_type)
    if not data:
        raise HTTPException(status_code=503, detail="Unable to fetch importation data or fallback.")
    return data
