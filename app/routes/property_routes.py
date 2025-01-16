from fastapi import APIRouter, Depends, HTTPException
from app.services.property_manager import PropertyManager
from app.utils.user import get_current_user
from app.services.property_search import PropertySearch
from typing import Optional, List
from app.models.property import PropertyDetails


router = APIRouter()

property_manager = PropertyManager()
property_search = PropertySearch(property_manager)

@router.post("/properties", status_code=201)
async def create_property(
    property_data: PropertyDetails, current_user: str = Depends(get_current_user)
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

        properties = await property_search.search_properties(criteria)

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit
        paginated_properties = properties[start_idx:end_idx]

        return {
            "properties": [p.to_dict() for p in paginated_properties],
            "total": len(properties),
            "page": page,
            "limit": limit,
            "total_pages": (len(properties) + limit - 1)
        }
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.post("/properties/{property_id}/shortlist", status_code=200)
async def shortlist_property(
    property_id: str,
    current_user: str = Depends(get_current_user)
):
    try:
        success = await property_search.shortlist_property(current_user, property_id)
        if not success:
            raise HTTPException(
                status_code=400,
                detail="Property not available for shortlisting"
            )
        return {"message": "Property shortlisted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")



@router.get("/properties/shortlisted", response_model=List[dict], status_code=200)
async def get_shortlisted_properties(
    current_user: str = Depends(get_current_user)
):
    try:
        properties = await property_search.get_shortlisted(current_user)
        return [p.to_dict() for p in properties]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
