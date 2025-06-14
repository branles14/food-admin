import pytest

from src.cli import main as cli_main


def run_cli(args, monkeypatch, tmp_db):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_db}")
    parser = cli_main.build_parser()
    parsed = parser.parse_args(args)
    outputs = []

    def fake_print(obj):
        outputs.append(obj)

    monkeypatch.setattr("builtins.print", fake_print)
    parsed.func(parsed)
    return outputs


@pytest.fixture()
def tmp_db(tmp_path):
    db = tmp_path / "test.db"
    return db


def test_cli_add_update_delete(monkeypatch, tmp_path, tmp_db):
    add_out = run_cli(
        [
            "add",
            "--product",
            "1",
            "--quantity",
            "2",
            "--tags",
            "dairy",
        ],
        monkeypatch,
        tmp_db,
    )
    added = add_out[0]
    cid = added["id"]

    update_out = run_cli(
        ["update", str(cid), "--quantity", "3", "--tags", "dairy,open"],
        monkeypatch,
        tmp_db,
    )
    updated = update_out[0]
    assert updated["quantity"] == 3
    assert updated["tags"] == ["dairy", "open"]

    delete_out = run_cli(["delete", str(cid)], monkeypatch, tmp_db)
    assert delete_out[0] == {"deleted": True}


def test_cli_update_extra_and_serve(monkeypatch, tmp_db):
    add_out = run_cli(
        [
            "add",
            "--product",
            "2",
            "--quantity",
            "1",
        ],
        monkeypatch,
        tmp_db,
    )
    cid = add_out[0]["id"]

    update_out = run_cli(
        [
            "update",
            str(cid),
            "--product",
            "3",
            "--quantity",
            "4",
            "--opened",
            "--remaining",
            "0.75",
            "--expiration-date",
            "2025-12-12",
            "--location",
            "shelf",
            "--tags",
            "a,b",
            "--container-weight",
            "50",
        ],
        monkeypatch,
        tmp_db,
    )
    up = update_out[0]
    assert up["quantity"] == 4
    assert up["location"] == "shelf"

    called = {}

    def fake_run(app, host, port):
        called["app"] = app
        called["host"] = host
        called["port"] = port

    monkeypatch.setattr(cli_main.uvicorn, "run", fake_run)
    run_cli(["serve"], monkeypatch, tmp_db)
    assert called["app"] == "src.api.app:app"
