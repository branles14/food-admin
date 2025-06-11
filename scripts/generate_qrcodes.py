import os
import pathlib
import qrcode
from services import container_service


def run():
    containers = container_service.list_containers()
    out_dir = pathlib.Path("qrcodes")
    out_dir.mkdir(exist_ok=True)
    for c in containers:
        file_path = out_dir / f"{c['uuid']}.png"
        qrcode.make(c["uuid"]).save(file_path)
        print("Generated QR for", c["uuid"])


if __name__ == "__main__":
    run()
