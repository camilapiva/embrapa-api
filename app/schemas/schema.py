from pydantic import BaseModel
from typing import Optional

class CommercializationItem(BaseModel):
    """Commercialization model."""

    category: str
    product: str
    quantity: int

class CommercializationResponse(BaseModel):
    """Commercialization response model."""
    commercializations: list[CommercializationItem]

class ProcessingItem(BaseModel):
    """Commercialization model."""

    grape_type: str
    category: str
    product: str
    quantity: int

class ProcessingResponse(BaseModel):
    """Commercialization response model."""
    processings: list[ProcessingItem]

class ProductionItem(BaseModel):
    """Production model."""

    category: str
    product: str
    quantity: int

class ProductionResponse(BaseModel):
    """Production response model."""
    productions: list[ProductionItem]

class ImportationItem(BaseModel):
    """Import model."""

    grape_type: str
    country: str
    quantity: int
    value: int

class ImportationResponse(BaseModel):
    """Import response model."""
    imports: list[ImportationItem]

class ExportationItem(BaseModel):
    """Export model."""

    grape_type: str
    country: str
    quantity: int
    value: int

class ExportationResponse(BaseModel):
    """Export response model."""
    exports: list[ExportationItem]
