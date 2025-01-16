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


