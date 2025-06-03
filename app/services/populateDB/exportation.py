from app.services.extractions.exportation import fetch_exportation_data
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from app.models.exportation import Exportation


async def populate_exportations(year: int):

    async with AsyncSessionLocal() as session:
        response = fetch_exportation_data(year)
        data = response.exportations
        try:
            await session.execute(delete(Exportation).where(Exportation.year == year))
            
            for item in data:
                grape_type = item.grape_type
                country = item.country
                quantity = item.quantity
                value = item.value
                year = year

                record = Exportation(
                    grape_type=grape_type,
                    country=country,
                    quantity=quantity,
                    value=value,
                    year=year
                )
                session.add(record)

            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e