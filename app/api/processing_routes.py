from fastapi import APIRouter, Query, HTTPException, Depends
from app.core.auth import get_current_user
from app.scraping.processing import fetch_processing_data
from typing import Literal

router = APIRouter(prefix="/processing", tags=["Processing"])

# Tipos válidos de uva conforme o site da Embrapa
GrapeType = Literal["subopt_01", "subopt_02", "subopt_03", "subopt_04"]

@router.get("/", dependencies=[Depends(get_current_user)])
def get_processing_data(
    year: int = Query(..., ge=1970, le=2023),
    grape_type: GrapeType = Query(..., alias="type")
):
    """
    Retorna os dados de processamento vitivinícola para o ano e tipo de uva especificados.
    Exemplo: /processing/?year=2022&type=subopt_01
    """
    data = fetch_processing_data(year, grape_type)
    if not data:
        raise HTTPException(
            status_code=503,
            detail="Unable to fetch processing data from Embrapa or fallback."
        )
    return data
