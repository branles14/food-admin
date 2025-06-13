from __future__ import annotations

import os
from typing import Any, List, Optional
from pydantic import BaseModel

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlite3 import Connection

from src.db import get_db
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


def db_conn() -> Connection:
    return get_db()


@app.get("/health")
def health(db: Connection = Depends(db_conn)) -> JSONResponse:
    try:
        db.execute("SELECT 1")
        return JSONResponse({"status": "ok"})
    except Exception as exc:  # pragma: no cover - simple healthcheck
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/containers")
def list_containers(db: Connection = Depends(db_conn)) -> Any:
    return container_service.list_containers(db)


@app.post("/containers", status_code=201)
def create_container(data: ContainerCreate, db: Connection = Depends(db_conn)) -> Any:
    return container_service.create_container(db, data.dict(exclude_unset=True))


@app.patch("/containers/{id}")
def update_container(
    id: Any, data: ContainerUpdate, db: Connection = Depends(db_conn)
) -> Any:
    container = container_service.update_container(
        db, id, data.dict(exclude_unset=True)
    )
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")
    return container


@app.delete("/containers/{id}")
def delete_container(id: Any, db: Connection = Depends(db_conn)) -> Any:
    if container_service.delete_container(db, id):
        return {"message": "Container deleted"}
    raise HTTPException(status_code=404, detail="Container not found")


if __name__ == "__main__":  # pragma: no cover
    port = int(os.environ.get("PORT", 3000))
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=port)
