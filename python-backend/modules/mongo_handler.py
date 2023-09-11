from pymongo import MongoClient
import os

class MongoHandler:
    DEFAULT_URI = "mongodb://localhost:27017/"

    def __init__(self, uri=None):
        if uri is None:
            uri = os.environ.get("MONGODB_URI", self.DEFAULT_URI)
        self.client = MongoClient(uri)
        self.db = None
        self.collection = None

    def connect(self, db_name, collection_name):
        """
        Connect to a specific database and collection.
        """
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, data):
        """
        Insert a new document into the collection.
        """
        if not self.collection:
            raise ValueError("Collection not set. Please call 'connect' first.")
        return self.collection.insert_one(data).inserted_id

    def fetch_all(self, query={}):
        """
        Fetch all documents matching a query from the collection.
        """
        if not self.collection:
            raise ValueError("Collection not set. Please call 'connect' first.")
        return list(self.collection.find(query))

    def update(self, query, new_data):
        """
        Update documents matching the query in the collection.
        """
        if not self.collection:
            raise ValueError("Collection not set. Please call 'connect' first.")
        return self.collection.update_many(query, {"$set": new_data}).modified_count

    def remove(self, query):
        """
        Remove documents matching the query from the collection.
        """
        if not self.collection:
            raise ValueError("Collection not set. Please call 'connect' first.")
        return self.collection.delete_many(query).deleted_count

# Example usage:
# handler = MongoHandler("mongodb://localhost:27017/")
# handler.connect("WeatherDB", "Forecasts")
# handler.insert({"location": "NY", "forecast": "sunny"})
