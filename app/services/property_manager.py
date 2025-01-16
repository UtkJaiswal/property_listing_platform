import uuid
from app.models.property import Property
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


    async def _update_indices(self, property_obj: Property):
        async with self.index_lock:
            
            price = property_obj.details.price
            if price not in self.price_index:
                self.price_index[price] = set()
            self.price_index[price].add(property_obj.property_id)
            
            
            location = property_obj.details.location.lower()
            if location not in self.location_index:
                self.location_index[location] = set()
            self.location_index[location].add(property_obj.property_id)
            
            
            prop_type = property_obj.details.property_type.lower()
            if prop_type not in self.type_index:
                self.type_index[prop_type] = set()
            self.type_index[prop_type].add(property_obj.property_id)
            
            
            self.status_index["available"].add(property_obj.property_id)


    async def add_property(self, user_id: str, property_details: dict) -> str:
        property_id = str(uuid.uuid4())
        property_obj = Property(property_id, user_id, property_details)

        async with self.property_lock:
            self.properties[property_id] = property_obj

            async with self.portfolio_lock:
        
                if user_id not in self.user_portfolios:
                    self.user_portfolios[user_id] = set()

                self.user_portfolios[user_id].append(property_id)

        await self._update_indices(property_obj)

        return property_id
    

    async def update_property_status(self, property_id: str, new_status: str, user_id: str) -> bool:

        if property_id not in self.properties:
            raise HTTPException(status_code=404, detail="Property not found")
        

        property_obj = self.properties[property_id]
        
        if property_obj.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this property")
        
        if new_status not in self.status_index:
            raise ValueError(f"Invalid status: {new_status}")
        

        async with property_obj.lock:

            async with self.index_lock:
                
                self.status_index[property_obj.status].remove(property_id)
                
                
                await property_obj.update_status(new_status)
                
                
                self.status_index[new_status].add(property_id)
        
        return True
    

    
    async def get_user_properties(self, user_id: str) -> List[Property]:

        async with self.portfolio_lock:
            property_ids = self.user_portfolios.get(user_id, set()).copy()

        properties = []

        for pid in property_ids:
            if pid in self.properties:
                properties.append(self.properties[pid])


        return sorted(properties, key=lambda p: p.created_at, reverse=True)
