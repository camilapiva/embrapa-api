from fastapi import APIRouter, Query, Depends, HTTPException
from app.scraping.exportation import fetch_exportation_data
from app.core.auth import get_current_user

router = APIRouter(prefix="/exportation", tags=["Exportation"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_exportation_data(
    year: int = Query(..., ge=1970, le=2023),
    export_type: str = Query(..., pattern="^subopt_0[1-4]$")
):
    """
    Retorna os dados de exportação para o ano e tipo especificados.
    """
    data = fetch_exportation_data(year, export_type)
    if not data:
        raise HTTPException(status_code=503, detail="Unable to fetch exportation data or fallback.")
    return data
