from __future__ import annotations

import os
from typing import Any, List, Optional
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.concurrency import run_in_threadpool
from sqlite3 import Connection

from src.db import get_inventory_db, get_product_db
from src.services import container_service


class ContainerCreate(BaseModel):
    product: Optional[Any] = None
    quantity: Optional[int] = None
    opened: Optional[bool] = None
    remaining: Optional[float] = None
    expiration_date: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None
    container_weight: Optional[int] = None


class ContainerUpdate(ContainerCreate):
    pass


app = FastAPI()


async def inventory_conn() -> Connection:
    return get_inventory_db()


async def product_conn() -> Connection:
    return get_product_db()


@app.get("/health")
async def health(db: Connection = Depends(inventory_conn)) -> JSONResponse:
    try:
        await run_in_threadpool(db.execute, "SELECT 1")
        return JSONResponse({"status": "ok"})
    except Exception as exc:  # pragma: no cover - simple healthcheck
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/containers")
async def list_containers(
    inv_db: Connection = Depends(inventory_conn),
    prod_db: Connection = Depends(product_conn),
) -> Any:
    return await run_in_threadpool(
        container_service.list_containers,
        inv_db,
        prod_db,
    )


@app.post("/containers", status_code=201)
async def create_container(
    data: ContainerCreate,
    inv_db: Connection = Depends(inventory_conn),
    prod_db: Connection = Depends(product_conn),
) -> Any:
    return await run_in_threadpool(
        container_service.create_container,
        inv_db,
        prod_db,
        data.dict(exclude_unset=True),
    )


@app.patch("/containers/{id}")
async def update_container(
    id: Any,
    data: ContainerUpdate,
    inv_db: Connection = Depends(inventory_conn),
    prod_db: Connection = Depends(product_conn),
) -> Any:
    container = await run_in_threadpool(
        container_service.update_container,
        inv_db,
        prod_db,
        id,
        data.dict(exclude_unset=True),
    )
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    return container


@app.delete("/containers/{id}")
async def delete_container(
    id: Any, inv_db: Connection = Depends(inventory_conn)
) -> Any:
    deleted = await run_in_threadpool(
        container_service.delete_container,
        inv_db,
        id,
    )
    if deleted:
        return {"message": "Container deleted"}
    raise HTTPException(status_code=404, detail="Container not found")


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
