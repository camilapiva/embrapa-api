from fastapi import HTTPException
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.processing import Processing
from sqlalchemy.exc import SQLAlchemyError
from app.schemas.schema import ProcessingItem, ProcessingResponse


async def fetch_processings_from_db(year: int):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(
                select(Processing).where(Processing.year == year)
            )
            records = result.scalars().all()

            if not records:
                raise HTTPException(status_code=404, detail=f"No data found for year {year}")

            # Converte os dados do ORM para o schema esperado pela resposta da API
            data = [
                ProcessingItem(
                    grape_type=record.grape_type,
                    category=record.category,
                    product=record.product,
                    quantity=record.quantity
                )
                for record in records
            ]

            return ProcessingResponse(processings=data)

        except SQLAlchemyError as db_err:
            raise HTTPException(status_code=500, detail="Database error")