from models.property import Property
from asyncio import Lock
from typing import List, Dict, Set, Optional
from .property_manager import PropertyManager

class PropertySearch:
    
    def __init__(self, property_manager: PropertyManager):
        self.property_manager = property_manager
        self.user_shortlists: Dict[str, Set[str]] = {}
        self.shortlist_lock = Lock()


    def search_properties(self, criteria: dict) -> list[Property]:
        results = self.status_index["available"]

        if "min_price" in criteria or "max_price" in criteria:
            min_price = criteria.get("min_price", float("-inf"))
            max_price = criteria.get("max_price", float("inf"))

            results &= {
                pid for price, properties in self.price_index.items()
                if min_price <= price <= max_price for pid in properties
            }

        if "location" in criteria:
            results &= self.location_index.get(criteria["location"], set())

        
        if "property_type" in criteria:
            results &= self.type_index.get(criteria["property_type"], set())


        sorted_results = sorted(
            results, key=lambda pid: self.price_index[pid]
        )

        return sorted_results
    

    def shortlist_property(self, user_id: str, property_id: str) -> bool:

        if property_id not in self.status_index["available"]:
            return False
        

        if user_id not in self.user_shortlists:
            self.user_shortlists[user_id] = set()

        
        self.user_shortlists[user_id].add(property_id)

        return True
    

    def get_shortlisted(self, user_id: str) -> list[Property]:

        shortlisted_ids  = self.user_shortlists.get(user_id, set())
        
        return [
            self.property_storage[pid]
            for pid in shortlisted_ids 
            if pid in self.status_index["available"]
        ]
        