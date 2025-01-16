from datetime import datetime
from asyncio import Lock
from pydantic import BaseModel
from typing import Dict, List



class PropertyDetails(BaseModel):
    location: str
    price: float
    property_type: str
    description: str
    amenities: List[str]



class Property:
    def __init__(self, property_id: str, user_id: str, details: Dict):
        self.property_id = property_id
        self.user_id = user_id
        self.details = PropertyDetails(**details)
        self.status = "available"
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.lock = Lock()
