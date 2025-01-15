class PropertySearch:
    def __init__(self):
        self.price_index = {}
        self.location_index = {}
        self.type_index = {}
        self.status_index = {"available": set(), "sold": set()}
        self.user_shortlists = {}
        