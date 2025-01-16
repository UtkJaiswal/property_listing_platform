from datetime import datetime
from asyncio import Lock
from pydantic import BaseModel
from typing import Dict, List


# Pydantic model for property details
class PropertyDetails(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]


# Represents a property with additional metadata for indexing
class Property:
    def __init__(self, property_id: str, user_id: str, details: Dict):
        self.property_id = property_id
        self.user_id = user_id
        self.details = PropertyDetails(**details)
        self.status = "available"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.lock = Lock()
