# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| Latest commit on `main` | Yes |
| Older commits | Best effort |

## Local-Only API — Read Before Deploying

The FORGE FastAPI server (`src/forge/api_server.py`) implements **no
authentication, authorization, or rate limiting**. It is designed to run on
`127.0.0.1` for a single coach workstation.

- Do **not** expose port 8000 to untrusted networks or the public internet.
- If remote access is required, place it behind an authenticating reverse proxy
  (e.g., nginx + basic auth/OIDC) and bind uvicorn to localhost only.
- Program and athlete data persisted in `forge.db` (SQLite) may contain
  personal health information; protect the file with OS permissions and encrypt
  backups. Never commit real athlete data.

## Dependencies

- Backend: install from pinned requirements where available; review upgrades to
  FastAPI/uvicorn/pydantic before merging.
- Frontend: keep `forge_web/package-lock.json` committed; Dependabot/renovate
  alerts should be triaged within 30 days.

## Data & Content Safety

Training output is decision support for qualified S&C professionals, not
medical advice. Exercise records carry contraindication/pain-safe metadata
(see `docs/DATA_MODEL.md`); do not remove these fields from migrations.

## Reporting a Vulnerability

Open a private security advisory on the repository (GitHub → Security → Report
a vulnerability). Do not file public issues for security problems. Expect
acknowledgement within 5 business days.
