from bson import ObjectId
from typing import Any, Dict, List, Optional
from db import get_db


def _normalize(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
    db = get_db()
    result = db.products.insert_one(data)
    return get_product_by_id(result.inserted_id)


def get_product_by_id(id_: Any) -> Optional[Dict[str, Any]]:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    return _normalize(db.products.find_one({"_id": id_}))


def list_products() -> List[Dict[str, Any]]:
    db = get_db()
    return [_normalize(p) for p in db.products.find()]


def update_product(id_: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    db.products.update_one({"_id": id_}, {"$set": data})
    return get_product_by_id(id_)


def delete_product(id_: Any) -> bool:
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    result = db.products.delete_one({"_id": id_})
    return result.deleted_count == 1
