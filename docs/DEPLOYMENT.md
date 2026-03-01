# Deployment Notes

## Local (Mac/Linux)

1. Install Ollama and pull model:

```bash
brew install ollama
brew services start ollama
ollama pull llama3.1:8b-instruct-q4_K_M
```

2. Run API + web:

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

3. Reindex KB (optional but recommended):

```bash
curl -X POST http://localhost:8787/kb/reindex
curl http://localhost:8787/kb/stats
```

4. Open browser:

`http://localhost:8787`

## Handoff webhook (optional)

Set webhook to forward escalation requests to Telegram/Email/Zapier/n8n:

```bash
export HANDOFF_WEBHOOK_URL="https://your-webhook-endpoint"
python app.py
```

The UI `Request Human Handoff` button will call `/handoff` and forward payload if webhook is configured.

## Enterprise hardening (next)

- reverse proxy + TLS
- SSO / role auth
- request logs + SIEM forwarding
- PII redaction pipeline
