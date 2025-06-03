from sqlalchemy import Column, Integer, String
from app.models.base import Base



class Commercialization(Base):
    __tablename__ = "commercializations"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)


class Processing(Base):
    __tablename__ = "processings"

    id = Column(Integer, primary_key=True, index=True)
    grape_type = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)


class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
    product = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)   
    year = Column(Integer, nullable=False, index=True)

                                  
class Importation(Base):
    __tablename__ = "importations"

    id = Column(Integer, primary_key=True, index=True)
    grape_type = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)

class Exportation(Base):
    __tablename__ = "exportations"

    id = Column(Integer, primary_key=True, index=True)
    grape_type = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False, index=True)