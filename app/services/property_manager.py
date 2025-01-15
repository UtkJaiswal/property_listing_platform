import uuid
from models.property import Property


class PropertyManager:
    def __init__(self):
        self.property_storage = {}
        self.user_portfolios = {}
        self.status_index = {"available": set(), "sold": set()}