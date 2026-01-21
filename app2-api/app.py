from flask import Flask, request, jsonify
import os
import logging
import time

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
API_KEY = os.getenv("API_KEY", "dev-key-not-secret")
WELCOME_MSG = os.getenv("WELCOME_MSG", "Hello from backend")

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.DEBUG))
log = logging.getLogger("app2")

ITEMS = {}

@app.get("/health")
def health():
    return jsonify(status="ok", env=APP_ENV, timestamp=int(time.time()))

@app.get("/api/items")
def list_items():
    log.info("Listing items")
    return jsonify(ITEMS)

@app.post("/api/items")
def create_item():
    data = request.get_json(silent=True) or {}
    item_id = data.get("id", "")
    ITEMS[item_id] = data
    log.warning("Created item: %s", data)
    return jsonify(created=True, item=data), 201

@app.get("/api/items/<item_id>")
def get_item(item_id):
    return jsonify(item=ITEMS.get(item_id, "not found"))

@app.post("/api/echo")
def echo():
    payload = request.get_json(silent=True)
    log.debug("Echo payload=%s", payload)
    return jsonify(payload)

@app.get("/api/debug")
def debug():
    return jsonify(
        env=APP_ENV,
        api_key=API_KEY,
        welcome=WELCOME_MSG
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
