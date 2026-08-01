# FORGE Coach Console v1.1 — Real Coach Workflow Pass — Report

## 1. Files Changed

| File | Change | Part |
|---|---|---|
| `src/forge/artifact_store.py` | Added `coach_overrides` field to save, list, duplicate, and update operations. Extended allowed fields in `update_artifact`. Added merge logic for nested override updates. | 1 |
| `src/forge/api_server.py` | Extended `UpdateArtifactRequest` to accept `coach_overrides: Optional[dict]`. | 1 |
| `forge_web/src/types/ui.ts` | Added `CoachOverrides`, `ExerciseSwap`, `PrescriptionEdit` types. Added `coach_overrides` to `SavedProgramArtifact`. | 1 |
| `forge_web/src/components/program/blocks.tsx` | Rewrote `SessionCard` and `ExerciseRow` as controlled components: accept override props, inline swap/editing panels, call parent callbacks instead of local state. | 1 |
| `forge_web/src/components/program/modes/ProgramBuilderMode.tsx` | Accepts `overrides` and `onUpdateOverrides` props. Manages lock/note/swap/edit override state per session/exercise. | 1 |
| `forge_web/src/components/program/SavedProgramsDrawer.tsx` | Added search (by athlete name), sport filter, status filter, sort (newest/oldest/A-Z), better metadata (phase/weeks, override indicators). | 2 |
| `forge_web/src/components/program/modes/CompareMode.tsx` | Rewrote diff engine: added week structure changes, session count changes, exercise added/removed/swapped/prescription changes, coach override diffs, validation deltas. Changed from empty-state-only to show-only-changed diff. | 3 |
| `forge_web/src/components/LeftPanel.tsx` | Added client-side validation (athlete name required, numeric checks, range sanity `0–120`/`0–50`/`1–7`/`0–240`/`0–365`), inline errors with red styling, clean empty-string handling, blocks submission when invalid. | 4 |
| `forge_web/src/components/program/ProgramWorkspaceHeader.tsx` | Replaced timer-based `flashState` with real API-driven save states. Notes save on blur triggers actual PATCH, awaits response, shows saving/saved/error states. Error states preserve user text. | 5 |
| `forge_web/src/components/CenterPanel.tsx` | Extended props: `coachOverrides`, `onUpdateOverrides`, `reviewSaveState`. Passes override data to builder mode. Passes save state to header. | 1, 5 |
| `forge_web/src/App.tsx` | Added `coachOverrides` state, `overrideSaveState`, `reviewSaveState`. `handleUpdateOverrides` debounces and saves via PATCH on timer. `handleSelectSavedProgram` loads overrides. `handleMarkReviewed` drives real API-driven save state. | 1, 5 |
| `src/forge/test_api_integration.py` | Added 11 tests covering coach_overrides: present in save, listed, session locks persist, session notes persist, exercise swaps persist, prescription edits persist, merge on repeated update, reload preserves, duplicate resets, compare fields present. | testing |

## 2. What Each Part Delivered

### Part 1 — Make Builder interactions real

**Before:** Lock/swap/edit buttons were purely cosmetic — toggling local state with zero persistence. Changes disappeared on reload.

**After:**

- **Session lock state** — clicking the lock icon on a session card toggles a locked state. Locked sessions show amber highlight and disable hover actions. State is stored in `coach_overrides.session_locks` and persisted via debounced PATCH.
- **Exercise swap override** — clicking the swap icon opens an inline text input. Coach types a replacement exercise name. Swap stores `{original_name, new_name, new_family}` in `coach_overrides.exercise_swaps`. The card shows a "Swapped" badge and the new name in bold.
- **Prescription override** — clicking the edit icon opens a 3-field inline editor (sets/reps, load/RPE, rest). On apply, stores in `coach_overrides.prescription_edits`. Card shows "Edited" badge.
- **Session-level coach note** — clicking the note icon opens an inline input. Saved note displays in amber banner. Stored in `coach_overrides.session_notes`.
- **Override indicators** — swapped exercises show indigo left border and "Swapped" tag; edited exercises show amber left border and "Edited" tag; locked sessions show amber ring and "Locked" badge.
- **Reload persistence** — when an artifact is loaded from the backend, `coach_overrides` is restored from the saved artifact and all badges/markers re-appear.
- **Compare visibility** — overrides appear as diff items in Compare mode.

### Part 2 — Upgrade the Library into a usable workspace

**Before:** Basic drawer listing with status badge, delete button, and minimal metadata.

**After:**

- **Search** — text input filters by athlete name (case-insensitive).
- **Sport filter** — dropdown auto-populated from all unique sports in saved programs.
- **Status filter** — dropdown with all statuses (draft, reviewed, approved, archive).
- **Sort** — newest first, oldest first, A–Z by athlete name.
- **Better metadata** — goal, sport+role, mode, version, updated date with hover tooltip, week/phase label, and a "Has coach overrides" indicator when overrides exist.
- **Empty/not-found messaging** — shows relevant message for no-saved vs no-match states.

### Part 3 — Upgrade Compare into a real coaching diff

**Before:** Compared 4 high-level fields (weeks, frequency, goal, blueprint) and 2 weekly fields (type, conditioning). No session-level or exercise-level comparison.

**After:**

- **Week structure changes** — detected if a week was added/removed, changed week type, changed session count, changed sprint exposure, changed conditioning density.
- **Session/exercise changes** — per-session walkthrough of exercises: added exercises (green with +), removed exercises (red strikethrough with −), prescription changes (amber with ✏). Works across all session sections (main work, warmup, conditioning).
- **Coach override diffs** — shows when one artifact has coach overrides that the other doesn't.
- **Validation deltas** — shows which validations are new vs resolved in the current version.
- **Change count badge** — header shows total change count.
- **Clean diff view** — only shows changed items; unchanged fields are not rendered (reduces noise).

### Part 4 — Harden form validation and generation UX

**Before:** Only `athlete_name` empty check disabled the generate button. Numeric fields used `parseInt` with no validation.

**After:**

- **Client-side validation** — validates all numeric fields for actual numeric content. Range-sanity checks for age (0–120), training age (0–50), available minutes (0–240), frequency (1–7), days to match (0–365).
- **Inline error messaging** — red-styled fields with error text and AlertCircle icon. Error state on field shows red border + background.
- **Empty optional numeric handling** — `type="text"` with `inputMode="numeric"` to avoid browser-native number-spinner issues. Empty strings are sent as `''`, not `NaN` or `0`.
- **Submission block** — if any validation errors exist, the generate button shows a red summary bar ("N validation errors — fix to generate") and clicking does nothing.
- **Generation in progress** — existing behavior maintained with loading spinner + "Generating..." text.

### Part 5 — Make save/review state real and API-driven

**Before:** `flashState` used `setTimeout` to fake saving/saved states regardless of actual API outcome.

**After:**

- **Review save state** — `handleMarkReviewed` sets state to `saving`, awaits the PATCH, then sets `saved` on success or `error` on failure. Displayed inline on the Approve/Reviewed button via `SaveIndicator` component.
- **Notes save state** — blur handler on notes textareas calls `onUpdateNotes` (which returns `Promise<boolean>`), awaits the API, shows saving/saved/error inline next to the textarea label. Error state shows "Save failed — text preserved" message below the textarea. Text is not silently reverted.
- **Override save state** — debounced PATCH (500ms) with saving/saved/error states managed by `overrideSaveState`.
- **No fake "Saved"** — all save indicators reflect actual request lifecycle. If PATCH fails, the UI shows error, not "Saved".

## 3. Backend / API / Artifact Changes

### Artifact schema addition

New field on saved artifacts:

```json
"coach_overrides": {
  "session_locks": { "sess_0": true },
  "session_notes": { "sess_0": "Coach note text" },
  "exercise_swaps": { "ex_0": { "original_name": "Back Squat", "new_name": "Front Squat", "new_family": "Strength" } },
  "prescription_edits": { "ex_0": { "sets_reps": "4 x 8", "loading_method": "75% 1RM", "rest": "90s" } }
}
```

### API endpoint changes

`PATCH /api/programs/{id}` now accepts:

```json
{ "coach_overrides": { "session_locks": { "sess_0": true } } }
```

Overrides are **merged** on repeated updates (not replaced), so sending `session_locks` doesn't wipe `session_notes`.

`list_artifacts()` now includes `coach_overrides` (empty dict if none).

`duplicate_artifact()` resets overrides to `{}`.

### Schema version

Retained at `SCHEMA_VERSION = 1` since `coach_overrides` is additive (existing artifacts load without it and get `{}` by default).

## 4. Test Count / Verification

### Backend tests: 39 tests, all passing

- 14 existing serializers tests unchanged
- 14 existing artifact store tests unchanged
- **11 new coach override tests** specifically covering:

| Test | What it verifies |
|---|---|
| `test_coach_overrides_present_in_saved` | Saved artifact has `coach_overrides` field |
| `test_coach_overrides_in_listing` | List view includes `coach_overrides` |
| `test_update_coach_overrides_session_locks` | Session lock persists after update |
| `test_update_coach_overrides_session_notes` | Session note persists after update |
| `test_update_coach_overrides_exercise_swaps` | Exercise swap persists after update |
| `test_update_coach_overrides_prescription_edits` | Prescription edit persists after update |
| `test_coach_overrides_merge_on_repeated_update` | Repeated updates merge, not replace |
| `test_artifact_reload_preserves_overrides` | Load after save retains overrides |
| `test_duplicate_resets_coach_overrides` | Duplicate clears overrides |
| `test_coach_overrides_in_compare_fields` | Compare-relevant fields present after load |

### Frontend verification

- TypeScript: `tsc --noEmit` passes clean
- Production build: `vite build` succeeds
- No frontend test framework exists; manual verification checklist below

### Manual verification checklist

| # | Flow | Expected |
|---|---|---|
| 1 | Generate → Save draft | Artifact appears in library |
| 2 | Open saved → Add coach note → Reload | Note persists in header and session view |
| 3 | Lock a session → Reload | Lock badge visible, amber ring present |
| 4 | Swap an exercise → Reload | "Swapped" badge, new name shown |
| 5 | Edit prescription → Reload | "Edited" badge, new values shown |
| 6 | Library search/filter/sort | Filters/sorts work on saved programs list |
| 7 | Compare two artifacts | Week, session, exercise, override diffs shown |
| 8 | Submit empty athlete name | Validation blocks generation |
| 9 | Submit invalid age (e.g. 200) | Inline error "Age should be 0–120" |
| 10 | Click Approve while PATCH succeeds | "Saved" indicator shown |
| 11 | Click Approve while PATCH fails | "Save failed" indicator shown, status unchanged |
| 12 | Edit notes, blur while PATCH fails | Error message shown, text preserved |

## 5. Coach-Visible Changes

A serious S&C coach would notice:

1. **Lock a session** — click the lock icon on any session card. The card gets an amber border and ring. Hover actions disappear. Reload the artifact — still locked.
2. **Swap a sticking exercise** — hover a main-work exercise, click the swap icon (↻), type a replacement, hit enter. The card immediately shows the new name with "Swapped" badge in indigo. Reload — swap sticks.
3. **Adjust a prescription** — hover, click edit (✎), change sets/reps in the inline editor, hit apply. Card shows new values with "Edited" badge. Reload — edit persists.
4. **Add a coach note to a session** — click the note icon, type, hit enter or save. Note appears as amber banner. Reload — note persists.
5. **Find a past program** — open the Library drawer, type an athlete name, filter by sport, sort by newest. No more hunting through a flat list.
6. **Compare two programs** — switch to Compare mode, select a saved artifact. See exactly what changed: added/removed exercises highlighted in green/red, prescription changes in amber, week type changes, coach overrides flagged.
7. **Get feedback when saving** — the Approve button shows a spinner while saving, checkmark on success, red "Save failed" on error. Notes show the same inline feedback.
8. **Don't accidentally generate with bad data** — type "abc" in the age field, get an inline red error. The generate button shows a validation error count and won't fire.
9. **Search the library** — 20+ saved programs, search by name, filter by sport (rugby, tennis, cricket), sort by updated date.

## 6. Remaining Gaps

- **Debounce-only override persistence** — overrides auto-save after 500ms of inactivity. Not transactional. If the browser closes mid-debounce, the last change could be lost. A "Save Overrides" explicit button would close this.
- **No undo for overrides** — once swapped/edited, there's no "revert to original" button. The swap input allows typing the original name back, but it's not a single-click revert.
- **No multi-artifact compare** — Compare only supports current-vs-saved, not saved-vs-saved. The diff engine is capable of it but the UI dropdown only selects one comparison target.
- **No template/presets for exercise swap** — the swap input is free-text. A dropdown of same-family exercises from the exercise library would be stronger, but requires the exercise library to be accessible from the frontend (currently backend-only).
- **Library search is local-only** — filters and sorts are in-memory on the frontend. With 1000+ artifacts, this would need backend pagination and search. Not needed at current scale.
- **No loading states for library operations** — delete and load have no spinner. At current artifact sizes (small JSON files) this is fast enough, but could feel sluggish on larger artifacts.
- **Validation on optional numeric fields uses `inputMode="numeric"`** — works on mobile, but desktop users can still paste non-numeric text. The parse-and-reject approach in `onChange` handles this. Edge case: typing "1e2" passes validation as 100.

## 7. Final Answer

**Yes, this pass materially moves the Coach Console from a "demo shell" toward a "real coach workspace."**

The console now has:

- **Persistent coach controls** — lock, swap, edit, and note operations that survive reload
- **A usable library** — searchable, filterable, sortable program repository
- **Meaningful comparison** — exercise-level diffs with override awareness
- **Validation guardrails** — inline errors prevent bad data submission
- **Honest save feedback** — UI reflects actual API success/failure

**What still blocks it from being a production coach tool?**

1. No auth/workspace separation — all users see all programs
2. No PDF export for athlete delivery (currently HTML-only athlete view)
3. Single-user JSON file backend — no concurrency, no history, no rollback
4. No exercise library dropdown in the swap UI

These are beyond the scope of this pass, which was explicitly scoped to the 5 workflow parts above. Within that scope, the console is materially improved.
