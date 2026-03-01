from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder="../web", static_url_path="")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL = os.getenv("MODEL", "llama3.1:8b-instruct-q4_K_M")

SYSTEM_POLICY = """You are an enterprise local support assistant.
- Keep responses concise and practical.
- Do not expose secrets, tokens, or internal credentials.
- If uncertain, ask one clarifying question.
"""


@app.get("/")
def index():
    return send_from_directory("../web", "index.html")


@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])
    msgs = [{"role": "system", "content": SYSTEM_POLICY}] + messages
    payload = {"model": MODEL, "messages": msgs, "stream": False}
    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    out = r.json()
    return jsonify({"content": out.get("message", {}).get("content", "")})


@app.get("/health")
def health():
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        ok = r.status_code == 200
    except Exception:
        ok = False
    return jsonify({"ok": ok, "model": MODEL})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8787)
