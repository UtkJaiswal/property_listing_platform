from app.models.property import Property
from asyncio import Lock
from typing import List, Dict, Set
from .property_manager import PropertyManager

class PropertySearch:
    
    def __init__(self, property_manager: PropertyManager):
        self.property_manager = property_manager
        self.user_shortlists: Dict[str, Set[str]] = {}
        self.shortlist_lock = Lock()


    async def _filter_by_price(self, min_price: float, max_price: float) -> Set[str]:
        result = set()
        async with self.property_manager.index_lock:
            for price, properties in self.property_manager.price_index.items():
                if min_price <= price <= max_price:
                    result.update(properties)
        return result


    async def search_properties(self, criteria: dict) -> list[Property]:

        async with self.property_manager.index_lock:
            results = self.property_manager.status_index["available"].copy()
        

        if criteria.get("min_price") is not None or criteria.get("max_price") is not None:
                price_results = await self._filter_by_price(
                    criteria.get("min_price", float("-inf")),
                    criteria.get("max_price", float("inf"))
                )
                results &= price_results


        if criteria.get("location"):
                location_results = self.property_manager.location_index.get(
                    criteria["location"].lower(), set()
                )
                results &= location_results

        
        if criteria.get("property_type"):
                type_results = self.property_manager.type_index.get(
                    criteria["property_type"].lower(), set()
                )
                results &= type_results

        properties = [
            self.property_manager.properties[pid] 
            for pid in results
            if pid in self.property_manager.properties
        ]

        return sorted(properties, key=lambda p: p.details.price)
    

    async def shortlist_property(self, user_id: str, property_id: str) -> bool:
        async with self.shortlist_lock:
            async with self.property_manager.index_lock:
                if property_id not in self.property_manager.status_index["available"]:
                    return False

            if user_id not in self.user_shortlists:
                self.user_shortlists[user_id] = set()

            self.user_shortlists[user_id].add(property_id)
            return True
    

    async def get_shortlisted(self, user_id: str) -> List[Property]:
        async with self.shortlist_lock:
            shortlisted_ids = self.user_shortlists.get(user_id, set()).copy()
        
        async with self.property_manager.index_lock:
            available_shortlisted = shortlisted_ids & self.property_manager.status_index["available"]
        
        return [
            self.property_manager.properties[pid]
            for pid in available_shortlisted
            if pid in self.property_manager.properties
        ]
        