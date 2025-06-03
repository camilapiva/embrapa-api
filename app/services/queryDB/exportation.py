from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Exportation
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schema import ExportationItem, ExportationResponse


async def fetch_exportations_from_db(year: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Exportation).where(Exportation.year == year)
            )
            records = result.scalars().all()

            if not records:
                raise HTTPException(status_code=404, detail=f"No data found for year {year}")

            # Converte os dados do ORM para o schema esperado pela resposta da API
            data = [
                ExportationItem(
                    grape_type=record.grape_type,
                    country=record.country,
                    quantity=record.quantity,
                    value=record.value,
                )
                for record in records
            ]

            return ExportationResponse(exportations=data)

        except SQLAlchemyError as db_err:
            raise HTTPException(status_code=500, detail="Database error")