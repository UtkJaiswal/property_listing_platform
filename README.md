# Real Estate Property Platform

This is a real estate property platform that allows users to list, search, and shortlist properties.

## Features

- **Property Management**
  - Create properties with details like location, price, type, etc.
  - Manage property status (e.g., available, sold).

- **Property Search**
  - Search properties with filters like price range, location, and type.
  - Pagination for search results.

- **Shortlisting**
  - Shortlist available properties for easy access.

- **Health Check**
  - Verify if the API is running.


## Design Patterns Used
- **Singleton** Pattern: Ensures single instances of PropertyManager and PropertySearch.
- **Observer** Pattern: Implicit in how the property indices are updated when properties change.

## Data Structure Design

1. Property Listings Data

    - **Data Structure**: Dict[str, Property]
    - **Reasoning**: A dictionary is ideal because it allows fast lookup by property ID. The property data is stored with the key as the property_id, which enables efficient retrieval, updates, and status management.

2. User Portfolios

    - **Data Structure**: Dict[str, Set[str]]
    - **Reasoning**: Each user’s portfolio is represented by a set of property IDs. Using a set ensures that properties are unique within a user’s portfolio, and it supports efficient membership checks (e.g., for adding or removing properties). The outer dictionary allows fast lookups by user_id.

3. Shortlisted Properties

    - **Data Structure**: Dict[str, Set[str]]
    - **Reasoning**: Each user's shortlisted properties are stored in a set. This ensures uniqueness and allows efficient adding/removing of shortlisted properties. The dictionary enables quick access by user_id.

4. Search Indices

    - **Data Structure**: Dict[str, Set[str]] for location_index, type_index; Dict[float, Set[str]] for price_index; Dict[str, Set[str]] for status_index.
    - **Reasoning**: The indices are structured as dictionaries for efficient searching based on criteria like price, location, property type, and status. The use of sets ensures fast lookups and efficient filtering. The dictionary structure enables fast access to properties matching specific criteria.



### Search/Sort Implementation Strategy

#### Price Range Filtering

**Approach**:
Use the price_index to efficiently filter properties by price range. The price_index maps prices to sets of property IDs.
A helper function (_filter_by_price) iterates through the index and selects properties whose prices fall within the specified range.
This is efficient because the index allows for quick lookups by price and eliminates the need to check every property individually.


#### Location-Based Search

**Approach**:
Use the location_index which maps normalized location strings (lowercase) to sets of property IDs. This allows for efficient filtering by location.
If a location is provided in the search criteria, the index is queried to get the set of properties that match the location, and then these are further filtered based on other criteria.


#### Multiple Criteria Sorting

**Approach**:
The search filters properties based on various criteria such as price, location, and property type. After filtering, the properties are sorted by the chosen criteria (e.g., by price in ascending order).
The final sorting step ensures that users see the most relevant properties according to their preferences.


####  Search Result Pagination
**Approach**:
After filtering and sorting properties, implement pagination by slicing the list of properties based on the page and limit values from the request.
Pagination is handled by calculating the start and end indices based on the requested page and limit.


#### Performance Considerations
**Approach**:
Use indexing for efficient lookups and filtering. The indices (price, location, type, and status) ensure that search operations are fast, especially for large datasets.
Avoid scanning the entire dataset for each search operation. Instead, filter results using the indices and narrow down the search based on the provided criteria.
Use asynchronous operations (with async/await) to handle concurrent requests without blocking the event loop, ensuring better performance under load.


###  Indexing Strategy

**Price Index**:
Stores properties by price in a dictionary, where the key is the price and the value is a set of property IDs. This allows for efficient filtering based on price ranges.

**Location Index**:
Stores properties by location (normalized to lowercase). This enables efficient filtering of properties by location.

**Type Index**:
Stores properties by type (e.g., "house", "apartment"). This helps in filtering properties by type.

**Status Index**:
Maps each property status (e.g., "available", "sold") to a set of property IDs, allowing quick lookups to check the status of a property.


## Installation

### Prerequisites

- Python 3.12.3


### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/UtkJaiswal/property_listing_platform
   cd property_listing_platform
   ```

2. Create a virtual environment

    ```bash
    python -m venv venv
    ```

    - For Windows

        ```bash
        venv\Scripts\activate
        ```

    - Linux/Mac

        ```bash
        source venv/bin/activate
        ```

3. Installations

    ```bash
    pip install -r requirements.txt
    ```

4. Run server

    ```bash
    uvicorn app.main:app --reload
    ```

## Testing

- For testing with dummy data hit the GET API at `http://localhost:8000/test` and the logs are available in the terminal
