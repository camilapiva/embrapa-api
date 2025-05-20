from fastapi import APIRouter, HTTPException
from app.scraping.production import fetch_production_data

router = APIRouter(prefix="/production", tags=["Production"])

@router.get("/")
def get_production_data():
    try:
        data = fetch_production_data()
        return data
    except Exception:
        raise HTTPException(status_code=503, detail="Unable to fetch production data from Embrapa.")
