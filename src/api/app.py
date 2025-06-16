from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from src.db import JsonlDB, get_inventory_db, get_product_db
from src.services import item_service, product_info_service


class ItemCreate(BaseModel):
    product: Optional[Any] = None
    upc: Optional[str] = None
    name: Optional[str] = None
    nutrition: Optional[Dict[str, Any]] = None
    quantity: Optional[int] = None
    opened: Optional[bool] = None
    remaining: Optional[float] = None
    expiration_date: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    container_weight: Optional[int] = None


class ItemUpdate(ItemCreate):
    pass


class ConsumeAmount(BaseModel):
    amount: float


app = FastAPI()


async def inventory_conn() -> JsonlDB:
    return get_inventory_db()


async def product_conn() -> JsonlDB:
    return get_product_db()


@app.get("/health")
async def health(db: JsonlDB = Depends(inventory_conn)) -> JSONResponse:
    try:
        await run_in_threadpool(db.read_all)
        return JSONResponse({"status": "ok"})
    except Exception as exc:  # pragma: no cover - simple healthcheck
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/inventory")
async def list_items(
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    items = await run_in_threadpool(
        item_service.list_items,
        inv_db,
        prod_db,
    )
    if not items:
        return {"message": "Inventory empty"}
    return items


@app.post("/inventory", status_code=201)
async def create_item(
    data: ItemCreate,
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    try:
        return await run_in_threadpool(
            item_service.create_item,
            inv_db,
            prod_db,
            data.dict(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.patch("/inventory/{id}")
async def update_item(
    id: Any,
    data: ItemUpdate,
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    product = await run_in_threadpool(
        item_service.update_item,
        inv_db,
        prod_db,
        id,
        data.dict(exclude_unset=True),
    )
    if not product:
        raise HTTPException(status_code=404, detail="Item not found")
    return product


@app.post("/inventory/{id}/consume")
async def consume_item(
    id: Any,
    data: ConsumeAmount,
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    item = await run_in_threadpool(
        item_service.consume_item,
        inv_db,
        prod_db,
        id,
        data.amount,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/inventory/{id}")
async def delete_item(id: Any, inv_db: JsonlDB = Depends(inventory_conn)) -> Any:
    deleted = await run_in_threadpool(
        item_service.delete_item,
        inv_db,
        id,
    )
    if deleted:
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/inventory/uuid/{uuid}")
async def get_item_by_uuid(
    uuid: Any,
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    item = await run_in_threadpool(
        item_service.get_item_by_uuid,
        inv_db,
        prod_db,
        uuid,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.patch("/inventory/uuid/{uuid}")
async def update_item_by_uuid(
    uuid: Any,
    data: ItemUpdate,
    inv_db: JsonlDB = Depends(inventory_conn),
    prod_db: JsonlDB = Depends(product_conn),
) -> Any:
    item = await run_in_threadpool(
        item_service.update_item_by_uuid,
        inv_db,
        prod_db,
        uuid,
        data.dict(exclude_unset=True),
    )
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.delete("/inventory/uuid/{uuid}")
async def delete_item_by_uuid(
    uuid: Any, inv_db: JsonlDB = Depends(inventory_conn)
) -> Any:
    deleted = await run_in_threadpool(
        item_service.delete_item_by_uuid,
        inv_db,
        uuid,
    )
    if deleted:
        return {"message": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
