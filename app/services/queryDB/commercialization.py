from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.commercialization import Commercialization
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schema import CommercializationItem, CommercializationResponse


async def fetch_commercializations_from_db(year: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Commercialization).where(Commercialization.year == year)
            )
            records = result.scalars().all()

            if not records:
                raise HTTPException(status_code=404, detail=f"No data found for year {year}")

            # Converte os dados do ORM para o schema esperado pela resposta da API
            data = [
                CommercializationItem(
                    category=record.category,
                    product=record.product,
                    quantity=record.quantity
                )
                for record in records
            ]

            return CommercializationResponse(commercializations=data)

        except SQLAlchemyError as db_err:
            raise HTTPException(status_code=500, detail="Database error")