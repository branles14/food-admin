from bson import ObjectId
from typing import Any, Dict, List, Optional
from uuid import uuid4
from db import get_db
from . import product_service


def _normalize(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    if "product" in doc and isinstance(doc["product"], ObjectId):
        prod = product_service.get_product_by_id(doc["product"])  # returns normalized
        doc["product"] = prod
    return doc


def create_container(data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    data = data.copy()
    if "product" in data and isinstance(data["product"], str):
        data["product"] = ObjectId(data["product"])
    data.setdefault("uuid", str(uuid4()))
    result = db.containers.insert_one(data)
    return get_container_by_id(result.inserted_id)


def get_container_by_id(id_: Any) -> Optional[Dict[str, Any]]:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    return _normalize(db.containers.find_one({"_id": id_}))


def list_containers() -> List[Dict[str, Any]]:
    db = get_db()
    return [_normalize(c) for c in db.containers.find()]


def update_container(id_: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    db.containers.update_one({"_id": id_}, {"$set": data})
    return get_container_by_id(id_)


def delete_container(id_: Any) -> bool:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    result = db.containers.delete_one({"_id": id_})
    return result.deleted_count == 1
