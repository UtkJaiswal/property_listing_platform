from fastapi import APIRouter, Depends, HTTPException
from schemas.property_schemas import PropertyCreate
from services.property_manager import PropertyManager
from utils.user import get_current_user
from services.property_search import PropertySearch
from typing import Optional

router = APIRouter()

property_manager = PropertyManager()
property_search = PropertySearch(property_manager)

@router.post("/properties", status_code=201)
async def create_property(
    property_data: PropertyCreate, current_user: str = Depends(get_current_user)
):
    try:
        property_id = property_manager.add_property(current_user, property_data.model_dump())
        return {"message": "Property created successfully", "property_id": property_id}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/properties/search", status_code=200)
async def search_properties(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    location: Optional[str] = None,
    property_type: Optional[str] = None,
    page: int = 1,
    limit: int = 10
):
    try:
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail="Page and limit must be positive integers.")

        criteria = {
            "min_price": min_price,
            "max_price": max_price,
            "location": location,
            "property_type": property_type,
        }

        properties = property_search.search_properties(criteria)
        start = (page - 1) * limit
        end = start + limit

        if start >= len(properties):
            return {"properties": [], "total": len(properties)}

        return {"properties": properties[start:end], "total": len(properties)}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
