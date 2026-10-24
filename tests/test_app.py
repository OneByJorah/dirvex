import json
from datetime import datetime, timezone

import pytest

from app import create_app


@pytest.fixture
def feed(tmp_path):
    path = tmp_path / "status.json"
    rows = [
        {
            "Name": "DEMO-DC-01",
            "Replication": "Healthy",
            "SYSVOL": "OK",
            "LDAPBind": "Success",
            "Services": {"DNS": "Running"},
            "LastChecked": datetime.now(timezone.utc).isoformat(),
        }
    ]
    path.write_text(json.dumps(rows))
    return path, rows


def client(path, **config):
    return create_app(
        {"TESTING": True, "STATUS_PATH": str(path), "DEMO_MODE": False, **config}
    ).test_client()


def test_dashboard_uses_feed_and_refreshes_each_request(feed):
    path, rows = feed
    web = client(path)
    assert b"DEMO-DC-01" in web.get("/").data
    rows[0]["Name"] = "DEMO-DC-02"
    path.write_text(json.dumps(rows))
    assert b"DEMO-DC-02" in web.get("/").data
    assert b"DEMO-DC-01" not in web.get("/").data


def test_stopped_service_degrades_status(feed):
    path, rows = feed
    rows[0]["Services"]["DNS"] = "Stopped"
    path.write_text(json.dumps(rows))
    assert b"Degraded" in client(path).get("/public").data


@pytest.mark.parametrize("payload", ["", "invalid", "{}", "[]", '[{"Name": "x"}]'])
def test_invalid_feed_never_reports_healthy(tmp_path, payload):
    path = tmp_path / "status.json"
    path.write_text(payload)
    web = client(path)
    assert b"Unknown" in web.get("/public").data
    assert web.get("/readyz").status_code == 503
    assert web.get("/healthz").status_code == 200


def test_missing_feed_is_unknown(tmp_path):
    assert b"Unknown" in client(tmp_path / "missing").get("/public").data


@pytest.mark.parametrize(
    "stamp", ["bad", "2020-01-01T00:00:00Z", "2099-01-01T00:00:00Z"]
)
def test_invalid_stale_or_future_timestamps_are_unknown(feed, stamp):
    path, rows = feed
    rows[0]["LastChecked"] = stamp
    path.write_text(json.dumps(rows))
    assert b"Unknown" in client(path).get("/public").data


def test_healthy_feed_and_security_headers(feed):
    response = client(feed[0]).get("/public")
    assert b"Healthy" in response.data
    assert "default-src 'self'" in response.headers["Content-Security-Policy"]
    assert response.headers["Cache-Control"] == "no-store"
    assert b"Uptime" not in response.data


def test_feed_html_is_escaped(feed):
    path, rows = feed
    rows[0]["Name"] = "<script>alert(1)</script>"
    path.write_text(json.dumps(rows))
    body = client(path).get("/").data
    assert b"<script>" not in body
    assert b"&lt;script&gt;" in body


def test_demo_is_explicit_and_allows_static_sample(feed):
    path, rows = feed
    rows[0]["LastChecked"] = "2020-01-01T00:00:00Z"
    path.write_text(json.dumps(rows))
    assert b"DEMO" in client(path, DEMO_MODE=True).get("/").data
    assert client(path, DEMO_MODE=True).get("/readyz").status_code == 200


def test_oversized_feed_is_rejected(feed):
    assert client(feed[0], MAX_FEED_BYTES=10).get("/readyz").status_code == 503
