# FORGE Coach Console v1 — Hardening Pass Report

## 1. Files Changed

| File | What Changed | Why |
|---|---|---|
| `forge_web/src/components/program/ProgramActionsBar.tsx` | **Deleted** | Dead code — duplicate action bar, imported nowhere |
| `forge_web/src/types.ts` | Fixed `ProgramResponse` alias from `ProgramViewModel` to `RawProgramResponse` | Misleading type — callers expected the raw API shape, not the UI model |
| `forge_web/src/components/session/blocks.tsx` | Renamed `ExerciseRow` → `DocExerciseRow` | Name collision with `program/blocks.tsx`'s `ExerciseRow` — different prop interfaces caused import confusion |
| `forge_web/src/components/program/ProgramDocumentView.tsx` | Updated import to `DocExerciseRow`; replaced flat session rendering with week-grouped hierarchy | Document view previously omitted week grouping, showing a flat list instead of structured program |
| `forge_web/src/App.tsx` | Consolidated two document view paths into one computed `documentArtifact`; added mock fallback indicator in header; added `handleDelete`; wrapped 3 panels in `ErrorBoundary`; added delete wiring to `SavedProgramsDrawer` | Two separate paths had `as any` casts; mock mode was invisible; no delete pathway; no error recovery |
| `forge_web/src/components/program/ProgramWorkspaceHeader.tsx` | Added `useEffect` to sync local notes state when `coachNotes`/`internalNotes` props change | Stale closure — notes lost when loading a saved artifact |
| `forge_web/src/components/program/SavedProgramsDrawer.tsx` | Added `onDelete` prop + trash button per card (hover-reveal) | No way to delete saved programs from the UI |
| `forge_web/src/components/LeftPanel.tsx` | Injury flags: added chip-style tag display with per-tag remove buttons; cleaner placeholder | Comma-separated input was poor UX; no visual feedback for active flags |
| `forge_web/src/components/ErrorBoundary.tsx` | **New file** — React class component with `getDerivedStateFromError` + retry button | No error recovery — any runtime crash killed the entire app |
| `forge_web/package.json` | Added `@types/react@19` dev dependency | Required for proper ErrorBoundary class component typing; also fixed pre-existing `key` prop TS errors in 4 component files |

## 2. What Each Part Delivered

### Part 1 — UX Audit + Gap Hardening

- **Mock fallback indicator**: Amber "Mock Mode" badge appears in the top header bar when the backend is unreachable. Previously the fallback was completely silent.
- **Delete from library**: Each saved program card has a hover-reveal trash icon. Prevents accumulation of stale artifacts with no cleanup path.
- **Injury flags UX**: Flag input now shows chip-style tags below the input with per-tag `×` removal. No more error-prone comma-splitting.
- **Error boundaries**: Three `ErrorBoundary` wrappers (one per panel) prevent a single component crash from taking down the entire app. Each boundary has a retry button.
- **Consolidated document view**: Two separate `ProgramDocumentView` paths merged into one computed `documentArtifact` variable. No more `as any` casts on the preview path.

### Part 2 — Workspace Architecture Cleanup

- **Removed dead code**: `ProgramActionsBar.tsx` — 81 lines of duplicate action buttons, imported by nothing.
- **Fixed type alias**: `ProgramResponse` previously pointed to `ProgramViewModel` (the UI shape) when callers expected the raw API response. Now points to `RawProgramResponse`.
- **Resolved name collision**: `session/blocks.tsx` exported `ExerciseRow` with a different prop interface than `program/blocks.tsx`'s `ExerciseRow`. Renamed to `DocExerciseRow`.
- **Added @types/react**: Proper React type definitions fixed both the ErrorBoundary class component and 4 pre-existing `key` prop TypeScript errors in component files.

### Part 3 — Program Workspace v1 Polish

- **Fixed notes stale closure**: `ProgramWorkspaceHeader` now has `useEffect` hooks that sync `localCoachNotes`/`localInternalNotes` when the corresponding props change. Previously, loading a saved artifact left notes fields showing stale values from the previous artifact.
- **Document view week hierarchy**: `ProgramDocumentView` now renders weeks → sessions (grouped) instead of a flat session list. Matches `AthleteDeliveryMode`'s structure.

### Part 4 — Save/Reviewed/Notes Workflow Hardening

- **Delete handler**: `handleDelete` in `App.tsx` calls `apiDelete` for real backend or removes from local state for mock mode. Properly clears `activeArtifactId` if the deleted artifact was active.
- **Delete UI**: `SavedProgramsDrawer` now accepts `onDelete` and shows a trash button per card (hover-reveal, stops propagation to prevent accidental selection).
- **Document view paths consolidated**: Single `documentArtifact` computed value replaces the two overlapping `ProgramDocumentView` conditionals. No `as any` casts needed.

### Part 5 — Trial-Readiness Pass

- **Mock mode visibility**: Coaches running the UAT runner without a backend now see a clear "Mock Mode" indicator. Previously they were unknowingly viewing synthetic data.
- **Delete available**: Coaches can manage their saved programs — delete stale artifacts, keep only relevant ones for the trial.
- **Error recovery**: If a component crashes mid-trial, the error boundary catches it with a retry button. No hard refresh needed.

### Part 6 — Docs + Verification

- **Build passes**: `npm run build` — 0 errors, 1693 modules transformed.
- **TypeScript clean**: `tsc --noEmit` — 0 errors (was 8 before, 4 pre-existing `key` prop errors + 4 from ErrorBoundary).
- **Backend tests**: 40 Wave 11A tests pass unchanged.
- **Report written**: This document.

## 3. Verification

| Check | Result |
|---|---|
| Frontend build (`npm run build`) | ✅ Success — 329 KB JS, 46 KB CSS |
| TypeScript errors (`tsc --noEmit`) | ✅ 0 errors (was 8 before) |
| Backend tests (Wave 11A) | ✅ 40/40 pass |
| Manual flow: generate → render → save → reviewed toggle | ✅ All paths functional |
| Manual flow: library open → select → compare | ✅ Works |
| Manual flow: athlete delivery render | ✅ Properly nested under weeks |
| Manual flow: UAT runner open | ✅ Works |
| Manual flow: print/PDF | ✅ Document view renders |

## 4. Coach-Visible Changes

A coach using the app after this pass will notice:

1. **"Mock Mode" badge** in the header when backend is unreachable — no more confusion about whether they're seeing real data.
2. **Delete buttons** on saved programs — hover over a program card to see the trash icon. Stale artifacts can be cleaned up.
3. **Error resilience** — if one panel crashes, the other two keep working. A retry button restores the crashed panel.
4. **Injury flags as chips** — typed flags appear as removable tags below the input. Click `×` to remove a flag without re-typing the whole list.
5. **Notes don't get lost** — loading a saved artifact correctly populates the coach notes textarea. Previously the old notes would persist.
6. **Document print shows weeks** — the print/PDF view now groups sessions under week headings, matching what the coach sees in the Athlete Delivery view.

## 5. Remaining Gaps

1. **Lock/swap/edit in Builder mode are cosmetic only** — the lock toggle, swap badge, and edit badge in `program/blocks.tsx` are UI-local state with no persistence. Refreshing the page loses them. A coach expecting to actually modify exercises will be misled.
2. **No search/filter in library** — `SavedProgramsDrawer` lists all programs with no search bar, no status/sport/date filters. With many saved programs, the list becomes hard to navigate.
3. **N+1 artifact loading on mount** — `apiList` returns summaries, then each is individually loaded via `apiLoad`. For a large artifact count this is slow. A batch-load endpoint would fix this.
4. **No form validation** — `LeftPanel` has no client-side validation beyond `athlete_name` required. Empty number fields use empty-string sentinels. No error messages on invalid input.
5. **Save indicator is timer-based** — the "saving → saved" animation in `ProgramWorkspaceHeader` uses `setTimeout`, not actual API response tracking. The UX is fine but the state is fake.
6. **No frontend test framework** — no Jest, Vitest, or Playwright setup. Only manual testing is possible. Recommended: add a minimal Vitest + React Testing Library setup for the transformers and API client.

## 6. Recommended Next Frontend Wave

1. **Make Builder interactions real** — wire lock/swap/edit to backend PATCH endpoints or at minimum persist session notes and exercise swaps.
2. **Add library search/filter** — even a simple text search on athlete name would dramatically improve the library UX.
3. **Batch artifact loading** — backend endpoint returning full artifacts in one call, or lazy-load only the selected artifact.
4. **Form validation layer** — add per-field validation (number ranges, required fields, sport/role format) with inline error messages.
5. **Frontend test framework** — Vitest + React Testing Library, start with `transformers.ts` and `api.ts` unit tests.
6. **Dark mode** — request from coaches reviewing at night. Tailwind v4 makes this mostly a theme-token change.
