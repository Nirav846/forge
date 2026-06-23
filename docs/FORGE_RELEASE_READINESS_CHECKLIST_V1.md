# FORGE Release Readiness Checklist v1

## Backend

- [x] All engine tests pass (425 tests, 0 failures)
- [x] 3 pre-existing failures fixed
- [x] API server starts cleanly on `:8000`
- [x] Health endpoint returns `{"status": "ok"}`
- [x] Generate endpoint returns valid contract for core + premium
- [x] Save/Load/List/Delete/Duplicate endpoints all return correct responses
- [x] PATCH endpoint for partial updates (status, notes)
- [x] Error handling — 404 returns structured `ErrorResponse`
- [x] Error handling — 500 returns structured `ErrorResponse` with traceback
- [x] CORS enabled for local dev
- [x] No uncaught exceptions during normal generation paths

## Frontend

- [x] `forge_web` compiles without new TypeScript errors
- [x] Generate button works with real backend
- [x] Loading spinner shows during generation
- [x] Block Builder view renders sessions with exercises
- [x] Coach Summary view shows rationale + personalization notes
- [x] Right panel shows Engine Intelligence (validation, rationale)
- [x] Right panel shows Engineering tab (Req JSON, Raw API, UI Model)
- [x] Save button persists to backend
- [x] Library drawer lists saved artifacts
- [x] Opening a saved artifact restores the program
- [x] Duplicate creates new artifact with +1 version
- [x] Reviewed/Draft badge updates and persists
- [x] Mock fallback works when backend is down
- [x] Error state renders coach-appropriate message (not stack trace)
- [x] Print/Delivery mode accessible
- [x] Compare mode accessible (load two artifacts)

## API Contract

- [x] `POST /api/programs/generate` accepts core + premium payloads
- [x] Response contains all 8 required top-level keys
- [x] Sessions contain `id`, `name`, `week_number`, `session_number`, `focus`, `warmup`, `main_work`, `conditioning`, `week_type`, `testing_markers`, `total_duration_min`, `load_capped`
- [x] Exercises contain `id`, `name`, `family`, `sets_reps`, `loading_method`, `rest`, `difficulty`, `equipment`
- [x] Summary contains all 11 documented fields
- [x] Metadata contains `generated_at`, `request_id`, `api_version`
- [x] Validation is always a list of `{type, message}` dicts (may be empty)
- [x] Rationale is always a list of strings (never empty)
- [x] Personalization notes is always a list of strings
- [x] Dropped constraints is always a list (currently empty)
- [x] API version `1.0.0`

## Save/Load

- [x] Artifact contains `schema_version` field
- [x] List view excludes full request/response payloads
- [x] Save → load preserves all fields
- [x] Duplicate creates independent artifact
- [x] Malformed artifact files silently skipped in list
- [x] Empty library returns `[]`
- [x] Schema version documented for future evolution
- [x] PATCH updates only whitelisted fields (status, notes)

## Print / Delivery

- [x] Browser print mode available (no server-side PDF)
- [ ] Delivery view hides internal engineering tab content (needs frontend check — print hides "Engineering" column)

## Tests

- [x] 29 API integration tests (23 original + 6 schema/update tests)
- [x] 40 Wave 10 stabilization tests
- [x] 425 engine tests (all passing, 0 failures)
- [x] Frontend TypeScript check: no new errors
- [x] Existing tests not broken by any change

## Docs

- [x] `FORGE_FRONTEND_API_CONTRACT_V1.md` — contract specification
- [x] `FORGE_PROGRAM_ARTIFACT_STORAGE_V1.md` — storage design
- [x] `FORGE_FRONTEND_BACKEND_INTEGRATION_VALIDATION_V1.md` — validation checklist
- [x] `FORGE_LOCAL_RUN_GUIDE_V1.md` — run commands
- [x] `FORGE_PROGRAM_ARTIFACT_SCHEMA_V1.md` — artifact schema spec
- [x] `FORGE_UAT_SCENARIO_PACK_V1.md` — UAT matrix
- [x] `FORGE_RELEASE_READINESS_CHECKLIST_V1.md` — this doc
- [x] `FORGE_WAVE10_STABILIZATION_AUDIT_V1.md` — audit report
- [x] `FORGE_WAVE10_IMPLEMENTATION_REPORT_V1.md` — implementation report

## Known Limitations (Release-Intentional)

- Weekly exposure detail shows "Not specified" — not blocking for v1 controlled testing
- Dropped constraints returns `[]` — not blocking for v1
- No server-side PDF — browser print sufficient for testing
- Exercise swap/edit not persisted — in-browser only
- Coach notes editor not wired to PATCH endpoint — notes can be saved via full save flow
- No auth/multi-user — single-user local only
- No athlete-facing delivery mode — coach-facing only
- Manual UAT not yet executed — automated tests only

## Not for v1

- Recovery/readiness systems
- Cloud sync / deployment
- Authentication / multi-user
- Real-time coach override persistence
- Exercise video library
- PDF generation server
- New engine features (Wave 11+)
