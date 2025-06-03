from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Importation(Base):
    __tablename__ = "importations"

    id = Column(Integer, primary_key=True, index=True)
    grape_type = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)