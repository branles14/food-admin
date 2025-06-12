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
        # Replace ObjectId with the complete product document
        prod = product_service.get_product_by_id(doc["product"])
        doc["product"] = prod
    return doc


def create_container(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a container entry and return the stored document.

    Parameters
    ----------
    data : Dict[str, Any]
        Container fields to persist.

    Returns
    -------
    Dict[str, Any]
        The created container with resolved product data.
    """
    db = get_db()
    data = data.copy()
    if "product" in data and isinstance(data["product"], str):
        data["product"] = ObjectId(data["product"])
    data.setdefault("uuid", str(uuid4()))
    result = db.containers.insert_one(data)
    return get_container_by_id(result.inserted_id)


def get_container_by_id(id_: Any) -> Optional[Dict[str, Any]]:
    """Return a container by its identifier.

    Parameters
    ----------
    id_ : Any
        Container ObjectId or string form.

    Returns
    -------
    Optional[Dict[str, Any]]
        The matching container or ``None`` when absent.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    return _normalize(db.containers.find_one({"_id": id_}))


def list_containers() -> List[Dict[str, Any]]:
    """Return all containers in the database.

    Returns
    -------
    List[Dict[str, Any]]
        List of container documents.
    """
    db = get_db()
    return [_normalize(c) for c in db.containers.find()]


def update_container(id_: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Update a container and return the modified document.

    Parameters
    ----------
    id_ : Any
        Container ObjectId or string form.
    data : Dict[str, Any]
        Fields to update on the container.

    Returns
    -------
    Optional[Dict[str, Any]]
        The updated container or ``None`` if not found.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    data = data.copy()
    if "product" in data and isinstance(data["product"], str):
        data["product"] = ObjectId(data["product"])
    db.containers.update_one({"_id": id_}, {"$set": data})
    return get_container_by_id(id_)


def delete_container(id_: Any) -> bool:
    """Delete a container by id.

    Parameters
    ----------
    id_ : Any
        Container ObjectId or string form.

    Returns
    -------
    bool
        ``True`` if a document was removed.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    result = db.containers.delete_one({"_id": id_})
    return result.deleted_count == 1
