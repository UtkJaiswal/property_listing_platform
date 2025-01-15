from fastapi import APIRouter, Depends, HTTPException
from schemas.property_schemas import PropertyCreate
from services.property_manager import PropertyManager
from utils.user import get_current_user

router = APIRouter()

property_manager = PropertyManager()

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
