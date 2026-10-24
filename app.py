"""Read-only domain-controller feed viewer; no domain credentials required."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from flask import Flask, render_template


def load_status(config):
    """Reject incomplete or stale feeds rather than claiming healthy systems."""
    try:
        with Path(config["STATUS_PATH"]).open("rb") as source:
            payload = source.read(config["MAX_FEED_BYTES"] + 1)
        if len(payload) > config["MAX_FEED_BYTES"]:
            raise ValueError("Feed exceeds size limit")
        rows = json.loads(payload.decode("utf-8-sig"))
        if not isinstance(rows, list) or not rows or len(rows) > 1000:
            raise ValueError("Expected 1-1000 controller records")
        controllers = []
        for row in rows:
            required = ("Name", "Replication", "SYSVOL", "LDAPBind", "LastChecked")
            if not isinstance(row, dict) or any(
                not isinstance(row.get(key), str) or not row[key].strip()
                for key in required
            ):
                raise ValueError("Incomplete controller record")
            services = row.get("Services")
            if (
                not isinstance(services, dict)
                or not services
                or any(
                    not isinstance(k, str) or not isinstance(v, str)
                    for k, v in services.items()
                )
            ):
                raise ValueError("Missing service states")
            checked = datetime.fromisoformat(row["LastChecked"].replace("Z", "+00:00"))
            if checked.tzinfo is None:
                raise ValueError("Timestamp must include timezone")
            age = (datetime.now(timezone.utc) - checked).total_seconds()
            stale = not config["DEMO_MODE"] and (
                age > config["STALE_AFTER_SECONDS"] or age < -60
            )
            healthy = (
                row["Replication"] == "Healthy"
                and row["SYSVOL"] == "OK"
                and row["LDAPBind"] == "Success"
                and all(v == "Running" for v in services.values())
            )
            controllers.append(
                {
                    **row,
                    "status": "Unknown"
                    if stale
                    else "Healthy"
                    if healthy
                    else "Degraded",
                }
            )
        overall = (
            "Unknown"
            if any(c["status"] == "Unknown" for c in controllers)
            else "Degraded"
            if any(c["status"] == "Degraded" for c in controllers)
            else "Healthy"
        )
        return {"controllers": controllers, "overall": overall, "error": None}
    except (OSError, ValueError, UnicodeError, RecursionError):
        return {
            "controllers": [],
            "overall": "Unknown",
            "error": "Status feed unavailable or invalid. Check collector output.",
        }


def create_app(config=None):
    app = Flask(__name__)
    app.config.update(
        STATUS_PATH=os.getenv(
            "STATUS_PATH", os.getenv("MOCK_PATH", "mock_dc_status.json")
        ),
        DEMO_MODE=os.getenv("DEMO_MODE", "true").lower() == "true",
        STALE_AFTER_SECONDS=int(os.getenv("STALE_AFTER_SECONDS", "900")),
        MAX_FEED_BYTES=1_048_576,
    )
    if config:
        app.config.update(config)
    if app.config["STALE_AFTER_SECONDS"] <= 0:
        raise ValueError("STALE_AFTER_SECONDS must be positive")

    @app.after_request
    def security_headers(response):
        response.headers.update(
            {
                "Content-Security-Policy": "default-src 'self'; object-src 'none'; "
                "base-uri 'none'; frame-ancestors 'none'",
                "X-Content-Type-Options": "nosniff",
                "Referrer-Policy": "no-referrer",
                "Cache-Control": "no-store",
            }
        )
        return response

    @app.get("/")
    def dashboard():
        return render_template(
            "dashboard.html", **load_status(app.config), demo=app.config["DEMO_MODE"]
        )

    @app.get("/public")
    def public():
        return render_template(
            "public.html", **load_status(app.config), demo=app.config["DEMO_MODE"]
        )

    @app.get("/healthz")
    def healthz():
        return "ok", 200

    @app.get("/readyz")
    def readyz():
        status = load_status(app.config)
        return status["overall"], 503 if status["overall"] == "Unknown" else 200

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
