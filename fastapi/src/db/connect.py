from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import dotenv_values

config = dotenv_values("../.env")
uri = config.get("MONGODB")


def connect_database():
    """Connection to Mongodb"""
    try:
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client["eventmanagement"]
    except Exception as e:
        print(f" Error connecting Mongo : {e}")
        return None