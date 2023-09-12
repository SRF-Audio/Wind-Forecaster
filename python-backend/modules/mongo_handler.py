from pymongo import MongoClient
import os

class MongoHandler:
    def __init__(self, uri=None):
        if uri is None:
            username = os.environ.get("MONGO_INITDB_ROOT_USERNAME", "admin")  # Default to "admin" if not found.
            password = os.environ.get("MONGO_INITDB_ROOT_PASSWORD", "pass")  # Default to "pass" if not found.
            host = os.environ.get("MONGO_HOST", "wind-forecaster-mongo")
            port = os.environ.get("MONGO_PORT", "27017")
            database = os.environ.get("MONGO_DB_NAME", "windForecaster")

            uri = f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"
            print(f"Using MongoDB credentials: {uri}")
        
        

        
        self.client = MongoClient(uri)
        self.db = None
        self.collections = {}
        
    def test_connection(self):
        """
        Test the connection to MongoDB.
        """
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            print("Successfully connected to MongoDB")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def connect(self, db_name, collection_names):
        """
        Connect to a specific database and set up collections.

        Args:
            db_name (str): Name of the database.
            collection_names (list): List of collection names to set up.
        """
        self.db = self.client[db_name]
        for col_name in collection_names:
            self.collections[col_name] = self.db[col_name]

    def insert(self, data, collection_name):
        """
        Insert a new document into the specified collection.
        """
        self._ensure_collection_exists(collection_name)
        return self.collections[collection_name].insert_one(data).inserted_id

    def fetch_all(self, collection_name, query={}):
        """
        Fetch all documents matching a query from the collection.
        """
        self._ensure_collection_exists(collection_name)
        return list(self.collections[collection_name].find(query))

    def update(self, collection_name, query, new_data):
        """
        Update documents matching the query in the collection.
        """
        self._ensure_collection_exists(collection_name)
        return self.collections[collection_name].update_many(query, {"$set": new_data}).modified_count

    def remove(self, collection_name, query):
        """
        Remove documents matching the query from the collection.
        """
        self._ensure_collection_exists(collection_name)
        return self.collections[collection_name].delete_many(query).deleted_count

    def is_forecast_present(self, collection_name, query={}):
        """
        Check if there are documents matching the query in the specified collection.
        """
        self._ensure_collection_exists(collection_name)
        return self.collections[collection_name].count_documents(query) > 0


    def _ensure_collection_exists(self, collection_name):
        """
        Internal method to check if a collection exists and raise an error if not.
        """
        if collection_name not in self.collections:
            raise ValueError(f"Collection '{collection_name}' not set. Please call 'connect' first.")
