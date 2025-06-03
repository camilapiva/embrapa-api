from app.services.extractions.processing import ProcessingExtractor
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from app.models.models import Processing


async def populate_processings(year: int):

    async with AsyncSessionLocal() as session:
        extractor = ProcessingExtractor()
        response = extractor.fetch_data(year)
        data = response.processings
        try:
            await session.execute(delete(Processing).where(Processing.year == year))
            
            for item in data:
                grape_type = item.grape_type
                category = item.category
                product = item.product
                quantity = item.quantity
                year = year

                record = Processing(
                    grape_type=grape_type,
                    category=category,
                    product=product,
                    quantity=quantity,
                    year=year
                )
                session.add(record)

            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e