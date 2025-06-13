from __future__ import annotations

import os
from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlite3 import Connection

from db import get_db
from services import container_service

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
def create_container(data: dict, db: Connection = Depends(db_conn)) -> Any:
    return container_service.create_container(db, data)


@app.patch("/containers/{id}")
def update_container(id: Any, data: dict, db: Connection = Depends(db_conn)) -> Any:
    container = container_service.update_container(db, id, data)
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
