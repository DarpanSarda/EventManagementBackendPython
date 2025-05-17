# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from dotenv import dotenv_values

# config = dotenv_values("../.env")
# uri = config.get("MONGODB")


# def connect_database():
#     """Connection to Mongodb"""
#     try:
#         # Create a new client and connect to the server
#         client = MongoClient(uri, server_api=ServerApi('1'))
#         client.admin.command('ping')
#         print("Pinged your deployment. You successfully connected to MongoDB!")
#         return client["eventmanagement"]
#     except Exception as e:
#         print(f" Error connecting Mongo : {e}")
#         return None

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values
from threading import Lock
import os


class MongoDBSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        """Ensure only one instance of MongoDB connection is created."""
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MongoDBSingleton, cls).__new__(cls)
                cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize MongoDB connection."""
        uri = os.environ.get("MONGODB")
        try:
            self.client = MongoClient(uri, server_api=ServerApi('1'))
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.db = self.client["eventmanagement"]
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_database(self):
        """Get the database instance."""
        return self.db

# Usage:
mongo_instance = MongoDBSingleton()
db = mongo_instance.get_database()