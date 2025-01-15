from pydantic import BaseModel
from typing import List, Optional

class PropertyCreate(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]
