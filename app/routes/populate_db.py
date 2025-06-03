from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.logging.logger import setup_logger
from app.services.populateDB.populate_all import populate_db


logger = setup_logger(__name__)
router = APIRouter(prefix="/populate_db", tags=["Database Population"])

@router.get("/", dependencies=[Depends(get_current_user)])
async def populate_database():
    """
    Endpoint to populate the database with data from all years.
    """
    await populate_db()
    return {"message": f"Database populated successfully"}