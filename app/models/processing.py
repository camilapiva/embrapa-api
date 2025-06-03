from sqlalchemy import Column, Integer, String
from app.models.base import Base


class Processing(Base):
    __tablename__ = "processings"

    id = Column(Integer, primary_key=True, index=True)
    grape_type = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)