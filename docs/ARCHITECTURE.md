# Architecture Overview

Local AI Support Suite is split into four layers:

## 1) API layer (`api/`)

- `POST /chat` — core chat endpoint (profile-aware)
- `POST /handoff` — records/escalates unresolved cases
- `POST /kb/reindex` — rebuild local retrieval index
- `GET /kb/stats` — retrieval visibility
- `GET /health` — runtime check

## 2) Policy layer

Profiles (`smb`, `web3`, `creator`) define assistant behavior and guardrails.

## 3) Knowledge layer (`kb/`)

- Local markdown/text knowledge files
- Indexed for retrieval grounding
- Designed for private deployment

## 4) Frontend layer (`web/`)

- Lightweight operator console
- Chat + profile switch + handoff trigger
- Contact and escalation UX

## Request flow

1. User message enters `/chat`
2. Profile prompt + KB context composed
3. Local model response returned
4. If unresolved, operator triggers `/handoff`
5. Handoff is logged and optionally forwarded via webhook

## Design principles

- Privacy first (local by default)
- Human override always available
- Small surface area, easy to deploy
- Auditability through logs and explicit handoff records
