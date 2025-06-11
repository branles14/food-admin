import os
from pymongo import MongoClient

_db = None
_client = None


def get_db():
    """Return a MongoDB database connection."""
    global _db, _client
    if _db is not None:
        return _db
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.environ.get("MONGODB_DB", "foodadmin")
    _client = MongoClient(uri)
    _db = _client.get_database(db_name)
    return _db
