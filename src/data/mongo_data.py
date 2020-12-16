from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase
from models.settings import get_settings

class MongoDatabase:
    mongo_client: AsyncIOMotorClient

def connect():
    # MongoDatabase.mongo_client = AsyncIOMotorClient('mongodb://admin:admin@localhost:27017')
    settings = get_settings()
    MongoDatabase.mongo_client = AsyncIOMotorClient(settings.mongo_connection_string)

def close():
    MongoDatabase.mongo_client.close()

def get_client() -> AsyncIOMotorClient:
    return MongoDatabase.mongo_client

def get_database() -> AsyncIOMotorDatabase:
    settings = get_settings()
    return MongoDatabase.mongo_client.get_database(settings.mongo_database_name)

def get_collection(collection_name: str) -> AsyncIOMotorCollection:
    database = get_database()
    return database.get_collection(collection_name)