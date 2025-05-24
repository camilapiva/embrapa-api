from fastapi import APIRouter, Query, HTTPException, Depends
from app.scraping.production import fetch_production_data
from app.core.auth import get_current_user

router = APIRouter(prefix="/production", tags=["Production"])

@router.get("/", dependencies=[Depends(get_current_user)])
def get_production_data(year: int = Query(..., ge=1970, le=2023)):
    """
    Retorna os dados de produção vitivinícola para o ano especificado.
    Exemplo: /production/?ano=2022
    """
    data = fetch_production_data(year)
    if not data:
        raise HTTPException(status_code=503, detail="Unable to fetch production data from Embrapa or fallback.")
    return data
