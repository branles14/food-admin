from flask import Flask, jsonify, request, send_file
import os
from bson import ObjectId
import io
import qrcode

from db import get_db
from services import container_service

app = Flask(__name__)

db = get_db()


@app.get("/health")
def health():
    try:
        db.command("ping")
        return jsonify({"status": "ok"})
    except Exception as exc:
        return jsonify({"status": "error", "message": str(exc)}), 500


@app.get("/containers")
def list_containers():
    return jsonify(container_service.list_containers())


@app.post("/containers")
def create_container():
    container = container_service.create_container(request.json or {})
    return jsonify(container), 201


@app.patch("/containers/<id>")
def update_container(id):
    container = container_service.update_container(id, request.json or {})
    if not container:
        return jsonify({"error": "Container not found"}), 404
    return jsonify(container)


@app.delete("/containers/<id>")
def delete_container(id):
    if container_service.delete_container(id):
        return jsonify({"message": "Container deleted"})
    return jsonify({"error": "Container not found"}), 404


@app.get("/containers/<id>/qrcode")
def container_qrcode(id):
    container = container_service.get_container_by_id(id)
    if not container:
        return jsonify({"error": "Container not found"}), 404
    img = qrcode.make(container["uuid"])
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
