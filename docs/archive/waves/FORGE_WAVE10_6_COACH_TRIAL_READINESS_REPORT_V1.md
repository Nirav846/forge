# FORGE Wave 10.6 — Coach Trial Readiness Report

## Overview

Wave 10.6 is the release-candidate hardening pass. It does not add new S&C
logic. It packages the existing engine (Waves 1–10.5) into something a
serious S&C coach or sports scientist can trial for real.

The trial surface: a local workstation running the FORGE Python backend +
React frontend. Single-user. JSON file–based artifact storage. No cloud,
no auth, no multi-user.

## What changed in Wave 10.6

1. **Save-state UX** — every PATCH-backed interaction (review status toggle,
   coach_notes, internal_notes) now shows saving/saved/error feedback
   instead of silent success-or-fail.
2. **UAT result export** — UAT runner can now download a JSON report of
   all pass/fail results for sharing or record-keeping.
3. **Athlete Delivery / Print hardening** — print layout gets consistent
   page breaks, metadata headers, cleaner exercise rows, and internal-only
   debug content removed from the athlete-facing view.
4. **Documentation pack** — 4 new docs (this report, PATCH wiring notes,
   UAT runner guide, coach trial script).

## Trial-ready capabilities

| Capability | Status |
|---|---|
| Generate 8-week programs (core + premium blueprints) | Ready |
| 16 sport roles with role-aware exposure targets | Ready |
| Youth safety cap (age < 20 capped at Intermediate) | Ready |
| Injury risk flags (lumbar, hamstring, patellar, shoulder, groin, ankle) | Ready |
| Force-velocity profile bias (force deficit / velocity deficit) | Ready |
| CMJ band, landing competency, sprint mechanics awareness | Ready |
| Session-level warmup + conditioning | Ready |
| Weekly exposure summary (sprint, jump/landing, decel, eccentric, cond) | Ready |
| Save / load / duplicate programs | Ready |
| Review workflow (draft → reviewed with status toggle) | Ready |
| Coach notes + internal notes per program | Ready |
| Compare two saved programs | Ready |
| Athlete-friendly delivery / print view | Ready (hardened in 10.6) |
| UAT scenario runner for structured testing | Ready (exportable in 10.6) |
| Print from browser to PDF | Ready (hardened in 10.6) |

## Known limitations

These are non-blocking for a controlled trial but worth documenting.

1. **Single-user, local only** — no cloud saves, no sharing. The coach runs
   one instance on their own machine.
2. **JSON file storage** — no database. Programs live in `.forge_artifacts/`
   next to the repo. Deleting that directory wipes all data.
3. **No undo** — save overwrites the artifact immediately. PATCH changes are
   immediate (no draft versioning within a single artifact).
4. **No mobile / tablet layout** — the frontend is desktop-only (three-panel
   layout needs ~1280 px width minimum).
5. **Warmup is program-level** — every session in a program gets the same
   warmup protocol rather than session-specific warmups.
6. **Testing markers are week-level** — the engine tags testing weeks but
   does not prescribe specific test protocols or re-test dates within the
   output.
7. **Exercise library is static** — exercises are drawn from a hardcoded
   library. No custom exercise creation or editing in the UI.

## Recommended coach trial flow

1. Install prerequisites (Python 3.12+, Node 20+).
2. Clone repo, install Python deps (`pip install -r requirements.txt`),
   install frontend deps (`cd forge_web && npm install`).
3. Start backend (`python run_forge_api.py`).
4. Start frontend (`cd forge_web && npm run dev`).
5. Open browser to `http://localhost:5173`.
6. Follow the coach trial script (`docs/FORGE_COACH_TRIAL_SCRIPT_V1.md`).

A full trial session is ~60–90 minutes covering 5–8 walkthrough tasks.

## Remaining post-trial backlog

- Session-specific warmup protocols
- Custom exercise creation
- Cloud / multi-user sync
- Undo / version history for artifacts
- Mobile-responsive layout
- Re-test scheduling and test-history tracking
- PDF export server-side (currently browser print → PDF)
