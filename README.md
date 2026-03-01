# Local AI Support Suite

Open-source toolkit to deploy **local/private AI customer support** for SMBs, Web3 communities, and content teams.

## Why

Most teams want AI support but cannot send sensitive customer data to third-party SaaS. This project helps deploy a private stack with controllable data boundaries.

## Core Features (v0.4)

- Local LLM backend (Ollama)
- Web chat widget/API
- Local knowledge-base retrieval (Markdown/TXT) with `/kb/reindex`
- Multi-profile policy packs: `smb`, `web3`, `creator`
- Human handoff endpoint + UI button (`/handoff`)
- Webhook-based escalation (`HANDOFF_WEBHOOK_URL`)
- Ops health checks (`/health`, `/kb/stats`)

## Target Users

- SMB customer support teams
- Web3 community operators
- Creator/content teams handling high-volume DMs

## Quick Start (draft)

```bash
# 1) start local model service
brew install ollama
brew services start ollama
ollama pull llama3.1:8b-instruct-q4_K_M

# 2) run api
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open `http://localhost:8787`.

## Roadmap

- [x] v0.1 scaffold
- [x] v0.2 RAG document index
- [x] v0.3 role-based policy profiles
- [x] v0.4 Human handoff via webhook
- [ ] v1.0 production deployment scripts + observability

## Contact

- WhatsApp: +60 18-783 9237
- Direct link: https://wa.me/60187839237
- Email: tom074738@gmail.com

## License

MIT
