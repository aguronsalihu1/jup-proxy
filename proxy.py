from flask import Flask, request, Response
import requests

app = Flask(__name__)

JUP_BASE = "https://quote-api.jup.ag"

@app.route("/<path:path>", methods=["GET", "POST"])
def proxy(path):
    """Relay all requests to Jupiter"""
    url = f"{JUP_BASE}/{path}"
    try:
        if request.method == "GET":
            r = requests.get(url, params=request.args, timeout=20)
        else:
            r = requests.post(url, json=request.json, timeout=20)
        return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type"))
    except Exception as e:
        return {"error": str(e)}, 500

@app.route("/")
def home():
    return {"message": "Jupiter Proxy is running!"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
