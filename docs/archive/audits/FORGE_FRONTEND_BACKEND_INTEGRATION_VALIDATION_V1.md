# FORGE Frontend–Backend Integration Validation v1

## Tested Flows (Automated)

### Backend API Tests (`src/forge/test_api_integration.py`)

| # | Test | Status |
|---|------|--------|
| 1 | Health endpoint returns ok | ✅ |
| 2 | POST /api/programs/generate with core payload returns valid contract | ✅ |
| 3 | POST /api/programs/generate with premium payload succeeds | ✅ |
| 4 | POST /api/programs/generate with minimal payload (no sport) succeeds | ✅ |
| 5 | POST /api/programs — save artifact returns valid record | ✅ |
| 6 | GET /api/programs — list returns saved artifacts | ✅ |
| 7 | GET /api/programs/{id} — load returns full artifact | ✅ |
| 8 | DELETE /api/programs/{id} — delete succeeds | ✅ |
| 9 | POST /api/programs/{id}/duplicate — duplicate succeeds | ✅ |
| 10 | GET /api/programs/nonexistent — returns 404 | ✅ |
| 11 | Serialization: GeneratedProgram → API JSON has all required fields | ✅ |
| 12 | Serialization: Session → API session has id, warmup, main_work, conditioning | ✅ |
| 13 | Serialization: Exercise → API exercise has name, sets_reps, loading_method, rest | ✅ |
| 14 | AthleteProfile from request: core fields mapped correctly | ✅ |
| 15 | AthleteProfile from request: risk flags mapped from injury list | ✅ |
| 16 | Generate with days_to_match triggers competition taper | ✅ |

### Frontend TypeScript Checks

| # | Check | Status |
|---|-------|--------|
| 1 | `api.ts` compiles without errors | ✅ |
| 2 | `App.tsx` compiles without errors | ✅ |
| 3 | `CenterPanel.tsx` compiles without errors | ✅ |

Note: 7 pre-existing TypeScript errors in `blocks.tsx` and `ProgramBuilderMode.tsx` (React `key` prop type issue with React 19 types) are unchanged by this integration pass.

## Manual QA Checklist

### Pre-flight
- [ ] Backend server is running on http://127.0.0.1:8000
- [ ] Frontend dev server is running on http://localhost:3000

### Generate Flow
- [ ] Enter athlete name, select sport, click "Generate"
- [ ] Loading spinner appears
- [ ] Program renders in Block Builder tab within 5-10 seconds
- [ ] Coach Summary tab shows rationale and personalization notes
- [ ] Right panel Intelligence tab shows validation and rationale
- [ ] Right panel Engineering tab shows Req JSON, Transform warnings, Raw API, UI Model
- [ ] Raw API tab shows the full backend JSON payload
- [ ] UI Model tab shows the normalized view model

### Save/Load Flow
- [ ] Click "Save" in the workspace header
- [ ] Library button shows count incremented
- [ ] Open Library drawer, saved artifact is listed
- [ ] Click on another scenario, generate, click Library
- [ ] Click on previously saved artifact → it loads and restores the program

### Compare Flow
- [ ] Save at least 2 artifacts
- [ ] Switch to Compare tab
- [ ] Select a saved artifact from the dropdown
- [ ] Structural delta shows differences

### Error Handling
- [ ] Stop the backend server, try to generate → error state shown
- [ ] Enter "error" as athlete name → simulated error (fallback)
- [ ] Enter "broken" as athlete name → malformed payload test (fallback)
- [ ] Try to load nonexistent artifact ID via API → 404

### Core vs Premium
- [ ] Core mode shows basic fields only
- [ ] Premium mode shows advanced profiling fields
- [ ] Both modes generate successfully

## Edge Cases Tested

| Edge Case | Expected Behavior | Status |
|-----------|------------------|--------|
| Empty athlete name (generate disabled) | Button disabled | ✅ |
| Spaces-only athlete name | Treated as empty | ✅ |
| Sport not recognized | Fallback to "athlete", generic blueprint | ✅ |
| Very short available_minutes (15) | Fewer program families | ✅ |
| days_to_match = 0 | Recovery program | ✅ |
| days_to_match = 1 | Light program | ✅ |
| days_to_match < 4 | Competition taper applied | ✅ |
| No advanced profile fields | Core program generated | ✅ |
| Injury risk flags with unrelated text | Only recognized risks mapped | ✅ |
| Malformed JSON in API request | 422 validation error | ✅ |

## What Remains Intentionally Unimplemented

1. **Full weekly exposure detail**: The backend's `program_exposure_summary()` computes exposure counts per week, but the API serializer currently outputs placeholder strings. This is a serializer enrichment task, not a missing backend capability.

2. **Persistent coach notes**: Coach notes can be added in the UI but are not saved to the artifact store. This requires adding note fields to the save endpoint and the frontend save flow.

3. **Exercise swap/edit persistence**: UI actions (swap/edit) are in-browser state only. Persisting these would require a "fork" or "override" model in the artifact store.

4. **Server-side PDF generation**: Browser print mode handles delivery. A server-side PDF engine would add significant complexity without improving the coaching use case.

5. **Authentication and multi-user**: Out of scope for this integration pass.

6. **Athlete-facing delivery mode simplification**: The Athlete Delivery mode currently renders the same view model as coach mode.
