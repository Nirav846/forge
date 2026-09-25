# FORGE — Elite Strength & Conditioning Program Generation System

FORGE (Framework for Optimized Resistance & Ground-based Exercise) is a
professional-grade Strength & Conditioning (S&C) platform that generates
periodized, sport-specific training programs with an offline-first React
coach console. Design philosophy: **"AI Enhanced, Never AI Dependent."**

> This README is the single entry point for the project. Detailed facts live
> in one authoritative document each (see [Documentation Map](#documentation-map)).

## What FORGE Generates

- 8-week periodized programs (Accumulation → Intensification → Realization → Test)
- Full session structure: warm-up (Raise–Activate–Potentiate), main work, conditioning
- Sport- and role-aware programming (e.g., Rugby Prop vs. Back)
- Detailed prescriptions: sets × reps, loading method (RPE/%1RM/BW), rest intervals,
  coach cues, and progression notes
- Credibility scoring and safety/validation checks against athlete profile

## Exercise Library (authoritative counts, as of 2026-09-24)

| Store | Contents | File |
|---|---|---|
| Backend engine data | 334 exercises | `src/forge/exercises_data.py` |
| Frontend library seed | 537 exercises, 222 complexes | `forge_web/src/data/exercises.json`, `complexes.json` |
| SQL migrations | Library phases through migration `000035` | `migrations/` |

See `docs/DATA_MODEL.md` for record schemas and how the stores relate.

## Architecture

```
forge engine (Python)            FastAPI server              React console
src/forge/                ->     src/forge/api_server.py ->  forge_web/
  main.py       generation         /api/programs*             Vite + TypeScript
  planning_engine.py               /api/teams/templates*      Tailwind
  session_assembly.py              /api/v1/exercises*         dnd-kit
  exercise_selector.py
  prescription_rules.py            SQLite (forge.db)
  progression_engine.py
  warmup_engine.py
  conditioning_engine.py
  recovery_engine.py
  substitution_engine.py
  time_constraint_engine.py
  role_profiles.py / blueprint_engine.py
```

## Quick Start

### Prerequisites

- Python 3.11+ with FastAPI/uvicorn installed
- Node.js 22+ and npm
- (Windows) helper scripts `start_forge.bat` / `stop_forge.bat` are provided

### Run the backend API

```bash
python run_forge_api.py        # serves http://127.0.0.1:8000
```

### Run the frontend

```bash
cd forge_web
npm install
npm run dev                    # development server
# or: npm run build && npm run preview -- --host 0.0.0.0 --port 3000
```

### Validate the environment / smoke test

```bash
python validate_forge_env.py
python smoke_check_forge.py
python run_forge_demo.py       # offline program generation demo
```

## Testing

- Backend engine tests: `pytest src/ tests/` (see `docs/TESTING.md` for the map of suites)
- Frontend tests: `npm run test` in `forge_web` (vitest)

## Deployment

The frontend deploys to GitHub Pages via `.github/workflows/deploy-pages.yml`
(builds `forge_web` on push to `main`). See `GITHUB_PAGES_GUIDE.md`.

## API Overview

| Endpoint group | Purpose |
|---|---|
| `GET /api/health` | Liveness check |
| `POST /api/programs/generate` | Generate a periodized program |
| `GET/DELETE /api/programs/{id}`, `POST .../duplicate` | Program management |
| `GET /api/teams/templates*` | Team template browsing/adaptation |
| `GET /api/v1/exercises[/search|/{id}]` | Exercise library queries with filters |

Full request/response schemas: `docs/API_REFERENCE.md`.

## Documentation Map

| Topic | Canonical document |
|---|---|
| System overview & verification checklist | `README_FORGE_SYSTEM.md`, `FORGE_SYSTEM_VERIFICATION.md` |
| Data model & library status | `docs/DATA_MODEL.md`, `EXERCISE_LIBRARY_STATUS.md` |
| Migration workflow | `docs/MIGRATIONS.md` |
| API reference | `docs/API_REFERENCE.md` |
| Frontend UI/responsive conventions | `docs/FRONTEND_UI_GUIDE.md` |
| Open plans / roadmap | `LIBRARY_ENHANCEMENT_PLAN.md`, `EXERCISE_LIBRARY_COMPLETION_PLAN.md` |
| Contribution workflow | `CONTRIBUTING.md` |
| Release history | `CHANGELOG.md` |
| Security policy | `SECURITY.md` |
| Doc audit & standards | `docs/DOCUMENTATION_AUDIT.md` |
| Historical reports (read-only) | `docs/archive/` |

## Disclaimer

FORGE outputs are training recommendations for qualified strength &
conditioning professionals. They are not medical advice; screen athletes and
adjust prescriptions per your organization's policies.
