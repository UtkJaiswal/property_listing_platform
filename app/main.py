from fastapi import FastAPI
from app.routes import property_routes
from app.services.property_manager import PropertyManager
from app.services.property_search import PropertySearch
import uvicorn


app = FastAPI(
    title="Real Estate Property Platform",
    description="A property listing and search platform",
    version="1.0.0"
)



property_manager = PropertyManager()
property_search = PropertySearch(property_manager)


app.include_router(
    property_routes.router,
    prefix="/api/v1",
    tags=["properties"]
)


@app.get("/test")
async def health_check():
    return {"status": "Working API"}


if __name__ == "__main__":
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )