from bson import ObjectId
from typing import Any, Dict, List, Optional
from db import get_db


def _normalize(doc: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not doc:
        return None
    doc["_id"] = str(doc["_id"])
    return doc


def create_product(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a product document and return the stored record.

    Parameters
    ----------
    data : Dict[str, Any]
        Fields of the product to persist.

    Returns
    -------
    Dict[str, Any]
        The created product with normalized ``_id``.
    """
    db = get_db()
    result = db.products.insert_one(data)
    return get_product_by_id(result.inserted_id)


def get_product_by_id(id_: Any) -> Optional[Dict[str, Any]]:
    """Retrieve a single product by its identifier.

    Parameters
    ----------
    id_ : Any
        Product ObjectId or its string form.

    Returns
    -------
    Optional[Dict[str, Any]]
        The matching product or ``None`` when not found.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    return _normalize(db.products.find_one({"_id": id_}))


def list_products() -> List[Dict[str, Any]]:
    """Return all products stored in the database.

    Returns
    -------
    List[Dict[str, Any]]
        Collection of product documents.
    """
    db = get_db()
    return [_normalize(p) for p in db.products.find()]


def update_product(id_: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Modify an existing product and return the updated record.

    Parameters
    ----------
    id_ : Any
        Product ObjectId or its string representation.
    data : Dict[str, Any]
        Fields to update on the product.

    Returns
    -------
    Optional[Dict[str, Any]]
        The updated product or ``None`` if not found.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    db.products.update_one({"_id": id_}, {"$set": data})
    return get_product_by_id(id_)


def delete_product(id_: Any) -> bool:
    """Remove a product from the database by id.

    Parameters
    ----------
    id_ : Any
        Product ObjectId or its string representation.

    Returns
    -------
    bool
        ``True`` if a document was deleted.
    """
    db = get_db()
    if isinstance(id_, str):
        id_ = ObjectId(id_)
    result = db.products.delete_one({"_id": id_})
    return result.deleted_count == 1
