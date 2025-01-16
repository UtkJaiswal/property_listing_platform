from app.services.property_manager import PropertyManager
from app.services.property_search import PropertySearch

property_manager = PropertyManager()
property_search = PropertySearch(property_manager)

async def manual_test():
    print("Starting manual testing...")

    print("\nAdding properties...")
    properties_to_add = [
        {
            "id": "1",
            "location": "Mumbai",
            "price": 500000,
            "property_type": "Apartment",
            "description": "Spacious apartment near Mannat",
            "amenities": ["Gym", "Pool"],
        },
        {
            "id": "2",
            "location": "Delhi",
            "price": 300000,
            "property_type": "House",
            "description": "Beautiful house in Delhi",
            "amenities": ["Garden", "Garage"],
        },
    ]

    last_property_id = ""

    for property_data in properties_to_add:
        try:
            property_id = await property_manager.add_property("1", property_data)
            last_property_id = property_id
            print(f"Property added: {property_id}")
        except Exception as e:
            print(f"Failed to add property: {e}")

    
    print("\nSearching for properties in Mumbai...")
    criteria = {
        "location": "Mumbai",
        "min_price": None,
        "max_price": None,
        "property_type": None,
    }
    try:
        results = await property_search.search_properties(criteria)
        print(f"Properties found: {results}")
    except Exception as e:
        print(f"Failed to search properties: {e}")

    print("\nShortlisting property with ID '1' for user...")
    try:
        success = await property_search.shortlist_property("1", last_property_id)
        if success:
            print("Property shortlisted successfully")
        else:
            print("Failed to shortlist property")
    except Exception as e:
        print(f"Error while shortlisting property: {e}")

    print("\nFetching shortlisted properties for user_id 1...")
    try:
        shortlisted_properties = await property_search.get_shortlisted("1")
        print(f"Shortlisted properties: {shortlisted_properties}")
    except Exception as e:
        print(f"Failed to fetch shortlisted properties: {e}")