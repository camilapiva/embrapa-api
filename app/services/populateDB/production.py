from app.services.extractions.production import ProductionExtractor
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import AsyncSessionLocal
from app.models.production import Production


async def populate_productions(year: int):

    async with AsyncSessionLocal() as session:
        extractor = ProductionExtractor()
        response = extractor.fetch_data(year)
        data = response.productions
        try:
            await session.execute(delete(Production).where(Production.year == year))
            
            for item in data:
                product = item.product
                quantity = item.quantity
                product_type = item.product_type
                year = year

                record = Production(
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