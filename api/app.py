from flask import Flask, request, jsonify, send_from_directory
import requests
import os
import re
from pathlib import Path
from typing import List, Dict

app = Flask(__name__, static_folder="../web", static_url_path="")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/chat")
MODEL = os.getenv("MODEL", "llama3.1:8b-instruct-q4_K_M")
KB_DIR = Path(os.getenv("KB_DIR", "../kb")).resolve()

BASE_POLICY = """You are an enterprise local support assistant.
- Keep responses concise and practical.
- Do not expose secrets, tokens, or internal credentials.
- If uncertain, ask one clarifying question.
- If knowledge snippets are provided, prioritize them and cite source file names.
"""

PROFILE_POLICIES = {
    "smb": """Profile: SMB support assistant.
- Prioritize faster resolution, clear next steps, and low technical jargon.
- Ask for order id, contact, and issue category when needed.
""",
    "web3": """Profile: Web3 community support assistant.
- Explain wallet/network/tx topics clearly and conservatively.
- Never request private keys or seed phrases.
- For security-sensitive issues, recommend official channels and verification steps.
""",
    "creator": """Profile: Creator support assistant.
- Focus on audience response, content ops, and publishing workflows.
- Keep answers concise and action-oriented.
""",
}

KB_INDEX: List[Dict[str, str]] = []


def tokenize(text: str) -> set:
    return set(re.findall(r"[a-zA-Z0-9_\-\u4e00-\u9fff]+", text.lower()))


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 120) -> List[str]:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i : i + chunk_size])
        i += max(1, chunk_size - overlap)
    return chunks


def rebuild_index() -> int:
    KB_INDEX.clear()
    KB_DIR.mkdir(parents=True, exist_ok=True)
    files = list(KB_DIR.glob("**/*.md")) + list(KB_DIR.glob("**/*.txt"))
    for p in files:
        try:
            raw = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for idx, ch in enumerate(chunk_text(raw), start=1):
            KB_INDEX.append(
                {
                    "source": str(p.relative_to(KB_DIR)),
                    "chunk_id": str(idx),
                    "text": ch,
                    "tokens": " ".join(sorted(tokenize(ch))),
                }
            )
    return len(KB_INDEX)


def retrieve(query: str, k: int = 4) -> List[Dict[str, str]]:
    q = tokenize(query)
    if not q or not KB_INDEX:
        return []
    scored = []
    for row in KB_INDEX:
        t = set(row["tokens"].split())
        inter = len(q & t)
        if inter == 0:
            continue
        score = inter / (len(q) ** 0.5 * (len(t) ** 0.5) + 1e-9)
        scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:k]]


@app.get("/")
def index():
    return send_from_directory("../web", "index.html")


@app.post("/chat")
def chat():
    data = request.get_json(force=True)
    messages = data.get("messages", [])

    profile = str(data.get("profile", "smb")).lower().strip()
    if profile not in PROFILE_POLICIES:
        profile = "smb"

    last_user = next((m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), "")
    refs = retrieve(last_user, k=4)
    ref_block = ""
    if refs:
        lines = []
        for r in refs:
            lines.append(f"[{r['source']}#{r['chunk_id']}] {r['text']}")
        ref_block = "\n\nKnowledge snippets:\n" + "\n".join(lines)

    system_policy = BASE_POLICY + "\n" + PROFILE_POLICIES.get(profile, PROFILE_POLICIES["smb"]) + ref_block
    msgs = [{"role": "system", "content": system_policy}] + messages
    payload = {"model": MODEL, "messages": msgs, "stream": False}
    r = requests.post(OLLAMA_URL, json=payload, timeout=180)
    r.raise_for_status()
    out = r.json()
    return jsonify({"content": out.get("message", {}).get("content", "")})


@app.post("/kb/reindex")
def kb_reindex():
    n = rebuild_index()
    return jsonify({"ok": True, "chunks": n, "kb_dir": str(KB_DIR)})


@app.get("/kb/stats")
def kb_stats():
    return jsonify({"chunks": len(KB_INDEX), "kb_dir": str(KB_DIR), "profiles": list(PROFILE_POLICIES.keys())})


@app.get("/health")
def health():
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=5)
        ok = r.status_code == 200
    except Exception:
        ok = False
    return jsonify({"ok": ok, "model": MODEL, "kb_chunks": len(KB_INDEX)})


if __name__ == "__main__":
    rebuild_index()
    app.run(host="0.0.0.0", port=8787)
