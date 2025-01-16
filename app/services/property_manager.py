import uuid
from models.property import Property
from datetime import datetime
from typing import Dict, List, Set
from fastapi import HTTPException
from asyncio import Lock



class PropertyManager:
    def __init__(self):
        self.properties: Dict[str, Property] = {}
        self.user_portfolios: Dict[str, Set[str]] = {}
        self.price_index: Dict[float, Set[str]] = {}
        self.location_index: Dict[str, Set[str]] = {}
        self.type_index: Dict[str, Set[str]] = {}
        self.status_index: Dict[str, Set[str]] = {
            "available": set(),
            "sold": set()
        }

        self.property_lock = Lock()
        self.index_lock = Lock()
        self.portfolio_lock = Lock()


    def add_property(self, user_id: str, property_details: dict) -> str:
        property_id = str(uuid.uuid4())
        property_object = Property(property_id, user_id, property_details)
        self.property_storage[property_id] = property_object
        
        if user_id not in self.user_portfolios:
            self.user_portfolios[user_id] = []

        self.user_portfolios[user_id].append(property_id)
        self.status_index["available"].add(property_id)

        return property_id
    

    def update_property_status(self, property_id: str, status: str, user_id: str) -> bool:
        property_obj = self.property_storage.get(property_id)
        
        if not property_obj or property_obj.user_id != user_id:
            return False
        
        self.status_index[property_obj.status].remove(property_id)

        property_obj.status = status

        self.status_index[status].add(property_id)

        return True
    
    def get_user_properties(self, user_id: str) -> list[Property]:
        property_ids = self.user_portfolios.get(user_id, [])
        return sorted(
            [self.property_storage[pid] for pid in property_ids],
            key = lambda p: p.timestamp,
            reverse=True
        )
