from pydantic import BaseModel, Field
from typing import Optional


class Car(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier")
    make: str = Field(..., description="Manufacturer")
    model: str = Field(..., description="Model name")
    year: int = Field(..., description="Model year")
    brand: str = Field(..., description="Brand name (used for search)")
    color: Optional[str] = Field(None, description="Optional color")


class CarCreate(BaseModel):
    make: str
    model: str
    year: int
    brand: str
    color: Optional[str] = None


class CarUpdate(BaseModel):
    make: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    brand: Optional[str] = None
    color: Optional[str] = None
