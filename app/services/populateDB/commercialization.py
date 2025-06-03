from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from app.services.extractions.commercialization import CommercializationExtractor 
from app.models.models import Commercialization


async def populate_commercializations(year: int):

    async with AsyncSessionLocal() as session:
        extractor = CommercializationExtractor()
        response = extractor.fetch_data(year)
        data = response.commercializations
        try:
            await session.execute(delete(Commercialization).where(Commercialization.year == year))
            
            for item in data:
                product = item.product
                quantity = item.quantity
                product_type = item.product_type
                year = year

                record = Commercialization(
                    product=product,
                    quantity=quantity,
                    product_type=product_type,
                    year=year
                )
                session.add(record)

            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e