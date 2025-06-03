from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)   
    year = Column(Integer, nullable=False, index=True)