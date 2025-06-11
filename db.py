import os
from pymongo import MongoClient
import mongomock

_db = None
_client = None


def get_db():
    """Return a MongoDB database connection."""
    global _db, _client
    if _db is not None:
        return _db
    uri = os.environ.get("MONGODB_URI")
    db_name = os.environ.get("MONGODB_DB", "foodadmin")
    if uri and not uri.startswith("mongomock://"):
        _client = MongoClient(uri)
    else:
        _client = mongomock.MongoClient()
    _db = _client.get_database(db_name)
    return _db
