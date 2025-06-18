from __future__ import annotations

import os
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from src.db import JsonlDB, get_inventory_db, get_product_db
from src.services import inventory_service, product_info_service


class ItemCreate(BaseModel):
    product: Optional[Any] = None
    upc: Optional[str] = None
    name: Optional[str] = None
    container_info: Optional[Dict[str, Any]] = None
    nutrition: Optional[Dict[str, Any]] = None
    opened: Optional[bool] = None
    weight_g: Optional[int] = None
    expiration_date: Optional[str] = None
    quantity: Optional[int] = None
    tags: Optional[List[str]] = None


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
) -> Any:
    items = await run_in_threadpool(
        inventory_service.list_items,
        inv_db,
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
            inventory_service.create_item,
            inv_db,
            prod_db,
            data.dict(exclude_unset=True),
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
