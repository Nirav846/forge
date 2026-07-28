# FORGE Local Run Guide v1

## Prerequisites

- Python 3.12+
- Node.js 18+
- npm

## Backend Setup

```bash
# From repo root (D:\forge)
cd D:\forge

# Install backend dependencies
pip install fastapi uvicorn pydantic

# Verify
python -c "from src.forge.main import generate_program"
```

The FORGE engine is pure Python with no external dependencies beyond FastAPI/uvicorn for the API server.

## Start Backend API Server

```bash
cd D:\forge
python run_forge_api.py
```

Server starts on `http://127.0.0.1:8000`.

Or directly via uvicorn:

```bash
cd D:\forge
python -m uvicorn src.forge.api_server:app --host 127.0.0.1 --port 8000 --reload
```

## Frontend Setup

```bash
cd D:\forge\forge_web
npm install
```

## Start Frontend Dev Server

```bash
cd D:\forge\forge_web
npm run dev
```

Server starts on `http://localhost:3000`.

## Generate a Test Program (End-to-End)

### Via the Web UI

1. Open `http://localhost:3000` in a browser
2. Enter athlete name (e.g. "Test Athlete")
3. Select sport (e.g. "rugby")
4. Click "Generate Program"
5. View the generated program in the center panel
6. Use the right panel to inspect raw API payload and normalized UI model

### Via the API Directly

```bash
curl -X POST http://127.0.0.1:8000/api/programs/generate \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "core",
    "basics": {
      "athlete_name": "John Smith",
      "sport": "rugby",
      "level": "Intermediate",
      "available_minutes": 60
    },
    "context": {
      "primary_goal": "strength"
    },
    "advanced": {}
  }'
```

## Save and Load a Program Artifact

```bash
# 1. Generate a program and capture the response
$response = curl -X POST http://127.0.0.1:8000/api/programs/generate ... | ConvertFrom-Json

# 2. Save the artifact
curl -X POST http://127.0.0.1:8000/api/programs \
  -H "Content-Type: application/json" \
  -d '{"request_payload":{...}, "response_payload":{...}}'

# 3. List saved artifacts
curl http://127.0.0.1:8000/api/programs

# 4. Load one artifact
curl http://127.0.0.1:8000/api/programs/{program_id}

# 5. Delete an artifact
curl -X DELETE http://127.0.0.1:8000/api/programs/{program_id}
```

Or using the web UI Library drawer (top-left "Library" button after generating).

## Running Tests

```bash
cd D:\forge
python -m unittest discover tests -v
```

API-specific tests:

```bash
cd D:\forge
python -m unittest src.forge.test_api_integration -v
```

## Known Limitations

### What Works
- Program generation from the web UI → real FORGE engine
- Artifact save/load/delete from the web UI → JSON file store
- Engineering console shows raw API payload, normalized UI model, transformer warnings
- Coach Summary mode shows rationale, personalization notes, weekly exposure mapping
- Block Builder shows sessions with warmup/main work/conditioning
- Compare mode shows structural diff between saved artifacts

### What Is Still Mocked or Partial
- **Weekly exposure details** (`sprint_exposure`, `jump_landing_exposure`, etc.): The backend computes these but the API serializer currently outputs `"Not specified"` placeholders. Full exposure detail requires deeper integration between the serializer and `program_exposure_summary()`.
- **Athlete delivery mode**: Uses the same view model as coach mode (no separate athlete-facing simplification).
- **Exercise swapping/editing**: UI actions (lock/swap/edit) are in-browser only, not persisted to backend.
- **Coach notes on sessions**: UI allows adding notes but they are not saved to artifacts.
- **PDF delivery**: Browser print is available; no server-side PDF generation.
- **Dropped constraints**: API returns empty array; backend doesn't currently surface constraint drop reasoning through the serializer.

### What Has Been Deferred
- Authentication
- User accounts
- Team management
- Cloud sync
- Recovery/readiness systems
- Exercise video library
- Real-time coach override persistence

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | `http://127.0.0.1:8000` | Backend API base URL (frontend .env) |

## Quick Start (Single Command)

```bash
# Terminal 1: Start backend
cd D:\forge && python run_forge_api.py

# Terminal 2: Start frontend
cd D:\forge\forge_web && npm run dev
```

Then open http://localhost:3000.
