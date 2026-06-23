# FORGE Local Run Guide v2

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm

## Validate Your Environment First (5s)

```bash
cd D:\forge
python validate_forge_env.py
```

All checks should show `PASS`. If any `FAIL`, follow the hint.

## Quick Start (One Command)

Double-click `start_forge.bat` — it launches both backend and frontend.

Or manually in two terminals:

```bash
# Terminal 1: Start backend
cd D:\forge && python run_forge_api.py
# Terminal 2: Start frontend
cd D:\forge\forge_web && npm run dev
```

| Service   | URL                          |
|-----------|------------------------------|
| Backend   | http://127.0.0.1:8000        |
| API Docs  | http://127.0.0.1:8000/docs   |
| Frontend  | http://localhost:3000         |

## Smoke Check

With the backend running, in a third terminal:

```bash
cd D:\forge && python smoke_check_forge.py
```

This pings `/api/health`, generates a sample program, saves/loads/deletes an artifact, and reports all-pass or the first failure.

## Configuration

| Variable      | Default                   | Description                     |
|---------------|---------------------------|---------------------------------|
| `VITE_API_URL`| `http://127.0.0.1:8000`   | Backend API base URL (frontend) |

## Full End-to-End Test

1. Open http://localhost:3000
2. Enter athlete name, select sport (e.g. "rugby"), click "Generate Program"
3. View generated program in center panel
4. Inspect raw payload and normalized model in the right panel

### Via API Directly

```bash
curl -X POST http://127.0.0.1:8000/api/programs/generate \
  -H "Content-Type: application/json" \
  -d '{"mode":"core","basics":{"athlete_name":"Test Athlete","sport":"rugby","level":"Intermediate","available_minutes":60},"context":{"primary_goal":"strength"},"advanced":{}}'
```

## Running Tests

```bash
cd D:\forge
python -m unittest discover tests -v
python -m unittest src.forge.test_api_integration -v
```

## Known Limitations

### Works
- Program generation via web UI or API → FORGE engine
- Artifact save/load/delete → JSON file store
- Engineering console (raw payload, normalized model, transformer warnings)
- Coach Summary mode (rationale, personalization, weekly exposure)
- Block Builder (sessions with warmup/main/conditioning)
- Compare mode (structural diff between saved artifacts)
- Weekly exposure details (sprint, jump/landing, agility, etc.)

### Still Mocked or Partial
- Athlete delivery mode (same view model as coach)
- Exercise locking/swapping/editing (in-browser only, not persisted)
- Coach notes on sessions (not saved to artifacts)
- PDF delivery (browser print only; no server-side PDF)
- Dropped constraints (API returns empty array)

### Deferred
- Auth, user accounts, team management, cloud sync
- Recovery/readiness systems, exercise video library
