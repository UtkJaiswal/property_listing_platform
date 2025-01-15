from pydantic import BaseModel
from typing import List, Optional

class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]


class PropertySearchCriteria(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    location: Optional[str] = None
    property_type: Optional[str] = None
    page: int = 1
    limit: int = 10