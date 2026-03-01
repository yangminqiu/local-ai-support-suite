# Contributing

Thanks for contributing to Local AI Support Suite.

## Development setup

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:8787` for the web UI.

## Branching

- Branch format: `feat/<short-name>`, `fix/<short-name>`, `docs/<short-name>`
- Keep PRs focused and small.

## Commit style

Use conventional-style prefixes:

- `feat:` new functionality
- `fix:` bug fix
- `docs:` docs only
- `chore:` tooling or housekeeping

## Pull request checklist

- [ ] Clear title and short rationale
- [ ] Steps to reproduce/test
- [ ] Backward compatibility considered
- [ ] Docs updated when behavior changes

## Scope

This project values practical, deployable improvements over demo-only changes.
