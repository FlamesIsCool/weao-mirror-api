from flask import Flask, jsonify
import requests
import time

app = Flask(__name__)

BASE_URL = "https://weao.xyz/api"
HEADERS = {"User-Agent": "WEAO-3PService"}

# ---- SIMPLE CACHE (prevents rate limit) ----
cache = {}
CACHE_TIME = 15  # seconds


def cached_get(url):
    now = time.time()
    if url in cache:
        data, timestamp = cache[url]
        if now - timestamp < CACHE_TIME:
            return data

    res = requests.get(url, headers=HEADERS)
    
    if res.status_code == 429:
        return {"error": "Rate limited by WEAO API"}, 429

    data = res.json()
    cache[url] = (data, now)
    return data


# --------------------------------------------------
#                EXPLOIT STATUS ROUTES
# --------------------------------------------------

@app.route("/api/exploits", methods=["GET"])
def all_exploits():
    url = f"{BASE_URL}/status/exploits"
    return jsonify(cached_get(url))


@app.route("/api/exploits/<name>", methods=["GET"])
def single_exploit(name):
    url = f"{BASE_URL}/status/exploits/{name}"
    return jsonify(cached_get(url))


# --------------------------------------------------
#                VERSION ROUTES
# --------------------------------------------------

@app.route("/api/versions/current", methods=["GET"])
def versions_current():
    url = f"{BASE_URL}/versions/current"
    return jsonify(cached_get(url))


@app.route("/api/versions/future", methods=["GET"])
def versions_future():
    url = f"{BASE_URL}/versions/future"
    return jsonify(cached_get(url))


@app.route("/api/versions/past", methods=["GET"])
def versions_past():
    url = f"{BASE_URL}/versions/past"
    return jsonify(cached_get(url))


# --------------------------------------------------
#                ROOT TEST ROUTE
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "online", "service": "WEAO mirror API"})


# --------------------------------------------------
#                START SERVER
# --------------------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
