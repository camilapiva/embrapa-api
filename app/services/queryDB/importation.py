from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.importation import Importation
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schema import ImportationItem, ImportationResponse


async def fetch_importations_from_db(year: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Importation).where(Importation.year == year)
            )
            records = result.scalars().all()

            if not records:
                raise HTTPException(status_code=404, detail=f"No data found for year {year}")

            # Converte os dados do ORM para o schema esperado pela resposta da API
            data = [
                ImportationItem(
                    grape_type=record.grape_type,
                    country=record.country,
                    quantity=record.quantity,
                    value=record.value,
                )
                for record in records
            ]

            return ImportationResponse(importations=data)

        except SQLAlchemyError as db_err:
            raise HTTPException(status_code=500, detail="Database error")