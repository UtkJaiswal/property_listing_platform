from datetime import datetime

class Property:
    def __init__(self, property_id: str, user_id: str, details: dict):
        self.property_id = property_id
        self.user_id = user_id
        self.details = details
        self.status = "available"
        self.timestamp = datetime.now()
