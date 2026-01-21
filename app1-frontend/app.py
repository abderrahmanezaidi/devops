from flask import Flask, request
import requests
import os
import logging

app = Flask(__name__)

API_URL = os.getenv("API_URL", "http://app2-api:5000")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.DEBUG))
log = logging.getLogger("app1")


@app.route("/items")
def items():
    return requests.get(f"{API_URL}/api/items").json()


@app.get("/")
def index():
    items = requests.get(f"{API_URL}/api/items").text
    debug = requests.get(f"{API_URL}/api/debug").text
    return f"""
    <h1>TP2 DevSecOps</h1>
    <h2>Create item</h2>
    <form method="POST" action="/create">
      <input name="id" placeholder="id"/>
      <input name="value" placeholder="value"/>
      <button>Create</button>
    </form>
    <h2>Items</h2><pre>{items}</pre>
    <h2>Backend debug</h2><pre>{debug}</pre>
    """

@app.post("/create")
def create():
    payload = {
        "id": request.form.get("id"),
        "value": request.form.get("value")
    }
    log.info("Sending payload %s", payload)
    requests.post(f"{API_URL}/api/items", json=payload)
    return ("", 302, {"Location": "/"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
