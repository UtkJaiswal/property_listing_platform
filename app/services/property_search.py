from app.models.property import Property
from asyncio import Lock
from typing import List, Dict, Set
from .property_manager import PropertyManager

# Logic for property search and management of user shortlists
class PropertySearch:
    
    def __init__(self, property_manager: PropertyManager):
        self.property_manager = property_manager
        self.user_shortlists: Dict[str, Set[str]] = {}
        self.shortlist_lock = Lock()

    # function for filtering by price
    async def _filter_by_price(self, min_price: float, max_price: float) -> Set[str]:
        result = set()
        async with self.property_manager.index_lock:
            for price, properties in self.property_manager.price_index.items():
                if min_price <= price <= max_price:
                    result.update(properties)
        return result


    # Function for searching properties based on multiple criteria and returns a sorted list of matching Property objects.
    async def search_properties(self, criteria: dict) -> list[Property]:

        async with self.property_manager.index_lock:
            results = self.property_manager.status_index["available"].copy()
        
        # Filter by price range if criteria provided
        if criteria.get("min_price") is not None or criteria.get("max_price") is not None:
                price_results = await self._filter_by_price(
                    criteria.get("min_price", float("-inf")),
                    criteria.get("max_price", float("inf"))
                )
                results &= price_results

        # Filter by location if criteria provided
        if criteria.get("location"):
                location_results = self.property_manager.location_index.get(
                    criteria["location"].lower(), set()
                )
                results &= location_results

        # filter by property type if criteria provided
        if criteria.get("property_type"):
                type_results = self.property_manager.type_index.get(
                    criteria["property_type"].lower(), set()
                )
                results &= type_results

        # Retrieve Property objects for the filtered property IDs
        properties = [
            self.property_manager.properties[pid] 
            for pid in results
            if pid in self.property_manager.properties
        ]

        # Sort the properties by price in ascending order
        return sorted(properties, key=lambda p: p.details.price)
    
    # Function to shortlist a property for a user and Returns True if the property was successfully shortlisted
    async def shortlist_property(self, user_id: str, property_id: str) -> bool:
        async with self.shortlist_lock:
            async with self.property_manager.index_lock:
                if property_id not in self.property_manager.status_index["available"]:
                    return False

            if user_id not in self.user_shortlists:
                self.user_shortlists[user_id] = set()

             # Add the property to the user's shortlist
            self.user_shortlists[user_id].add(property_id)
            return True
    
    # Function to get a user's shortlisted properties and returns  A list of Property objects that are currently available and shortlisted by the user.
    async def get_shortlisted(self, user_id: str) -> List[Property]:
        async with self.shortlist_lock:
            shortlisted_ids = self.user_shortlists.get(user_id, set()).copy()
        
        async with self.property_manager.index_lock:
            # Retain only properties that are still available
            available_shortlisted = shortlisted_ids & self.property_manager.status_index["available"]
        
        # Retrieve Property objects for the shortlisted property IDs
        return [
            self.property_manager.properties[pid]
            for pid in available_shortlisted
            if pid in self.property_manager.properties
        ]
        