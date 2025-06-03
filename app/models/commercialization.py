from sqlalchemy import Column, Integer, String
from app.models.base import Base



class Commercialization(Base):
    __tablename__ = "commercializations"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)