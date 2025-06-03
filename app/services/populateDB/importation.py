from app.services.extractions.importation import fetch_importation_data
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from app.models.importation import Importation


async def populate_exportations(year: int):

    async with AsyncSessionLocal() as session:
        response = fetch_importation_data(year)
        data = response.importations
        try:
            await session.execute(delete(Importation).where(Importation.year == year))
            
            for item in data:
                grape_type = item.grape_type
                country = item.country
                quantity = item.quantity
                value = item.value
                year = year

                record = Importation(
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