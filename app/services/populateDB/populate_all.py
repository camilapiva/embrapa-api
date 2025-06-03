from app.core.database import engine, Base
from app.services.populateDB.commercialization import populate_commercializations


async def populate_db():
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    for year in range(1970, 2024):
        await populate_commercializations(year)

    # for year in range(1970, 2024):
    #     await populate_processings(year)