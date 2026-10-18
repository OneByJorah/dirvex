import json
import os

from flask import Flask, render_template

app = Flask(__name__)

# Load demo DC status data (mock data only; no live AD required)
MOCK_PATH = os.environ.get("MOCK_PATH", "mock_dc_status.json")
try:
    with open(MOCK_PATH, "r") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []


@app.route("/")
def dashboard():
    return render_template("dashboard.html", dc_data=data)


@app.route("/public")
def public():
    return render_template("public.html")


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
