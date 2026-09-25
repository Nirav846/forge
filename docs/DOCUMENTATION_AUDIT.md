# FORGE Project Documentation Audit & Remediation Plan

**Audit Date:** 2026-09-24
**Auditor:** Technical Documentation Specialist
**Scope:** All Markdown documentation in the repository root, `docs/`, and `forge_web/`

---

## 1. Methodology

Every documentation file was inspected and cross-checked against the actual project state:

| Verified fact | Evidence |
|---|---|
| Frontend library contains **537 exercises + 222 complexes** | `forge_web/src/data/exercises.json` (537 items), `complexes.json` (222 items) |
| Backend exercise DB has **334 exercises** (7,708 lines) | `src/forge/exercises_data.py` |
| Migrations run through **000035** (32 up-migrations) | `migrations/` |
| API is **FastAPI-based**, endpoints under `/api/...` and `/api/v1/exercises...` | `src/forge/api_server.py` |
| GitHub Pages deploy workflow exists (Node 22, builds `forge_web`) | `.github/workflows/deploy-pages.yml` |
| No root `README.md` exists | filesystem check |

Key finding: the repository contains **~25 status/completion reports from overlapping, contradictory "phase" numbering schemes** (e.g., two different "Phase 7" documents; "Phase 2 complete = ~65 exercises" vs. "Exercise Library Status = 271" vs. audit reports citing 537). These are session artifacts, not living documentation.

---

## 2. Documentation Inventory & Disposition

### 2.1 REMOVE (obsolete, redundant, or no longer serving the project)

These files are point-in-time completion reports superseded by later phases and by the current data state. Keeping them causes active harm: contributors cite stale exercise counts and outdated architecture claims.

| # | File | Category | Justification |
|---|---|---|---|
| 1 | `PHASE2_COMPLETE_SUMMARY.md` | Remove | Claims "~65 exercises total"; superseded by Phases 3–9 and the 537-exercise library. Contradicts current data. |
| 2 | `PHASE3_COMPLETE_SUMMARY.md` | Remove | Claims "~115 exercises"; same contradiction. IDs 200–249 now overlap with migration 000028's Phase 3 range — actively confusing. |
| 3 | `PHASES_COMPLETE_SUMMARY.md` | Remove | Duplicates #1/#2 content with yet another numbering ("Phases 3, 4, 5 complete, ~280+"). Redundant. |
| 4 | `PHASE6_ELITE_LOCKER_ROOM_SUMMARY.md` | Remove | "~270+ exercises, 100% complete" snapshot superseded by Phases 7–9 and current 537-item library. |
| 5 | `PHASE7_COMPLETE_SUMMARY.md` | Remove | Overlaps with `PHASE_7_COMPLETE_SUMMARY.md` (see #6); duplicate topic with divergent claims. |
| 6 | `PHASE_7_COMPLETE_SUMMARY.md` | Remove | Duplicate of #5 under a different filename — evidence of unmanaged doc sprawl. |
| 7 | `PHASE9_CONDITIONING_COMPLETE.md` | Remove | One-off migration note for 000034 (18 exercises); superseded by 000035 and covered by the new Data Migration Guide (Create C-3). |
| 8 | `PHASE_1A_COMPLETION_REPORT.md` | Remove | UI feature-completion report; features are now simply the shipped app. Belongs in git history / release notes. |
| 9 | `PHASE_1B_COMPLETION_REPORT.md` | Remove | Same rationale as #8. |
| 10 | `PHASE_1C_COMPLETION_REPORT.md` | Remove | Same rationale as #8. |
| 11 | `PHASE_1E_COMPLETION_REPORT.md` | Remove | Contains placeholder date (`2025-01-XX`) — never finalized; same rationale as #8. |
| 12 | `STEP1_VERIFICATION_REPORT.md` | Remove | Verification snapshot tied to an old audit step; conclusions already reflected in shipped code. |
| 13 | `SETTINGS_SUMMARY.md` | Remove | First-person implementation memo ("I have conducted…"); Settings feature ships in the app; no ongoing reference value. |
| 14 | `ELITE_EXERCISE_LIBRARY_DEPLOYMENT.md` | Remove | "Phase 1 Deployment" report; entirely superseded by later phases and by README (Update U-1). |
| 15 | `LIBRARY_ENHANCEMENT_SUMMARY.md` | Remove | Completion summary duplicating `LIBRARY_ENHANCEMENT_PLAN.md`; its "Before vs After" numbers are stale. |
| 16 | `IMPLEMENTATION_GUIDE_QUICK_WINS.md` | Remove | Contains copy-paste code blocks targeting specific old file states (`CATEGORY_GROUPS` replacement snippet); will mislead once applied twice. Implemented work lives in code. |
| 17 | `CSCS_AUDIT_AND_REMEDIATION.md` | Remove* | Historical gap-analysis whose gaps are closed (library now 537). *If coaching-rationale provenance matters, archive to `docs/archive/` instead of deleting. |
| 18 | `EXERCISE_LIBRARY_COMPLEX_AUDIT_REPORT.md` | Remove* | Audit dated 2025-06-18; findings addressed per later summaries. Archive option as #17. |
| 19 | `UI_UX_LIBRARY_ANALYSIS_REPORT.md` | Remove* | Analysis feeding #16; recommendations now implemented. Archive option as #17. |
| 20 | `FORGE_SYSTEM_STATUS_REPORT.md` | Merge→Remove | Content duplicated by `FORGE_SYSTEM_VERIFICATION.md` and `README_FORGE_SYSTEM.md`; dated "December 2024". Fold any unique facts into the README, then delete. |
| 21 | `docs/prompts/run/run_forge_demo.py` | Move out of docs | Executable script stored as documentation with no accompanying explanation; duplicates root-level `run_forge_demo.py`. Move to repo root/scripts and reference it from the README. |

**Net effect:** 20 Markdown files removed (3 optionally archived), eliminating all mutually contradictory status snapshots.

### 2.2 UPDATE (retain but correct inaccuracies)

| # | File | Category | Required changes & justification |
|---|---|---|---|
| U-1 | `README_FORGE_SYSTEM.md` | Update | Becomes the canonical system overview (and should be renamed/copied to root `README.md` — see C-1). Fixes needed: (a) exercise-count claims must distinguish backend 334 vs frontend 537 + 222 complexes (currently vague/inconsistent); (b) architecture tree omits modules that exist today (`substitution_engine.py`, `recovery_engine.py`, `time_constraint_engine.py`, `conditioning_engine.py`, `team_store.py`, `artifact_store.py`, `api_serializers.py`); (c) document both API namespaces (`/api/programs*`, `/api/teams/templates*`, `/api/health` and `/api/v1/exercises*`); (d) remove "✅ System Status: FULLY OPERATIONAL" banner (status claims rot; move to CHANGELOG). Tone: neutral third person, no emoji in headings. |
| U-2 | `FORGE_SYSTEM_VERIFICATION.md` | Update | Retain only the durable parts: component/port table, verification checklist, sample curl commands. Delete promotional language ("COMPLETE, PRODUCTION-READY") and date-stamp results. Re-title as `docs/VERIFICATION_CHECKLIST.md` if kept separate from README; otherwise merge into README §Verification. |
| U-3 | `GITHUB_PAGES_GUIDE.md` | Update | Strip the embedded changelog (Sections "Exercise Library Button", "Branding Updates" — those are code changes, not deployment guidance). Keep/correct: workflow behavior (push to `main`, Node 22, `npm ci` in `forge_web`), the `base: '/forge/'` requirement in `vite.config.ts`, Pages source = GitHub Actions, and custom-path troubleshooting. Verify base path matches the live repo name before publishing. |
| U-4 | `EXERCISE_LIBRARY_STATUS.md` | Update | Stale headline ("Total Exercise Count: 271"; migrations listed only through Phase 7). Either refresh to current counts (537/222; migrations to 000035) **or** fold into the new `docs/DATA_MODEL.md` (C-2) and delete. Recommended: fold — one source of truth for library facts. |
| U-5 | `EXERCISE_LIBRARY_COMPLETION_PLAN.md` | Update | Open forward-looking plan (metadata fields, remaining categories) — keep, but re-baseline against reality: several listed gaps (coaching cues, common faults) are already populated in `exercises.json`; mark completed items done, convert remainder into a tracked TODO section. |
| U-6 | `LIBRARY_ENHANCEMENT_PLAN.md` | Update | Still the best roadmap document, but its "Current State" numbers predate Phases 8–9. Refresh the baseline, confirm whether the monolith split of `exercises_data.py` (7,708 lines) happened, and align phase numbering with the new consolidated scheme (see Recommendation R-2). |
| U-7 | `forge_web/UI_UX_IMPLEMENTATION_SUMMARY.md` | Update | Convert from completion report to a durable **reference**: describe the current super-category organization structure (`exerciseOrganization.ts`: 7 super-categories), filtering/search behavior, and modal UX contract — without "what was implemented" narrative. Relocate to `docs/FRONTEND_UI_GUIDE.md` (single home for docs). |
| U-8 | `forge_web/mobile_responsive_summary.md` | Update | Same conversion: becomes a standing "Responsive design conventions" section (breakpoints used, header nav behavior, mobile-first rules) merged into U-7's document. Lowercase filename → consistent naming. |

### 2.3 CREATE (fill identified gaps)

| # | New Document | Purpose & Key Content | Standards / Format |
|---|---|---|---|
| C-1 | `README.md` (repo root) | Entry point for the project — currently **absent**. Sections: What FORGE is; architecture diagram (engine → FastAPI → React console); quick start (backend `python run_forge_api.py` on :8000, frontend `npm install && npm run dev` in `forge_web`, Windows helpers `start_forge.bat`); tech stack (Python/FastAPI/SQLite + React 18/TypeScript/Vite/Tailwind); links to `docs/*`; license/disclaimer (not medical advice). | Keep ≤200 lines; imperative voice; fenced code blocks with language tags; badge-free until CI exists for tests. Content may be promoted from updated `README_FORGE_SYSTEM.md`. |
| C-2 | `docs/DATA_MODEL.md` | Single source of truth for exercise-library data: schema of an exercise record (fields incl. `coaching_cues`, `common_faults`, contraindications, development levels), authoritative counts (backend `exercises_data.py` = 334; frontend `exercises.json` = 537; `complexes.json` = 222), how the three stores (Python module, JSON seed, SQL migrations) relate and which wins at runtime, and known duplication risks. | Tables for field definitions; explicit "as of" date; verified against files at write time. |
| C-3 | `docs/MIGRATIONS.md` | How to add/modify library data: golang-migrate numbering convention (`NNNNNN_name.{up,down}.sql`, currently at 000035), idempotency rules, review checklist (movement pattern taxonomy, equipment tags, sport mapping), and the process for regenerating frontend JSON from migrations. Prevents the ID-collision problems visible between old Phase docs and migrations 000026–000035. | Numbered procedure; example migration skeleton; DoD checklist. |
| C-4 | `docs/API_REFERENCE.md` | Reference for every FastAPI endpoint actually present in `src/forge/api_server.py`: `/api/health`, `/api/programs` (list/get/duplicate), `/api/programs/generate`, `/api/teams/templates*`, `/api/v1/exercises` (+`/search`, `/{id}`) — request/response schemas, filters, error codes, examples (curl). Currently endpoint details are scattered across phase reports being removed. | REST reference style: method + path heading, parameter table, request/response JSON samples; generated examples validated against a running server. |
| C-5 | `CONTRIBUTING.md` | Dev workflow: branch/PR flow (repo uses PRs into `main`), environment setup, running pytest suites in `src/`, `tests/`, and vitest in `forge_web`, pre-checks (`validate_forge_env.py`, `smoke_check_forge.py`), and coding conventions. | Standard community-contributing layout; short, actionable. |
| C-6 | `docs/TESTING.md` | Map of the fragmented test assets: what `test_complete_system.py`, `_test_api_server.py`, `_test_serializer.py`, `validation_test.py`, `src/test_*.py`, `tests/test_wave*.py` cover, how to run each, and which underscore-prefixed files are deprecated generators (candidates for code cleanup by maintainers). Fills the gap left when verification reports (#12, #20, #21) are removed. | Table: file → scope → command → status. |
| C-7 | `CHANGELOG.md` | Forward-looking release history using Keep a Changelog format. Replaces the need for perpetual "PHASE X COMPLETE" files: each release gets one entry with library count deltas and migration IDs added. Seed with a single "Unreleased" section referencing migration 000035 as latest known change. | Keep a Changelog 1.1.0; SemVer. |
| C-8 | `SECURITY.md` | Minimal security policy: local-only API assumptions, no authentication on `/api/*` (explicit warning not to expose publicly), SQLite file handling (`forge.db`), dependency update process. Expected by GitHub/community standards; currently missing. | GitHub security-policy template, ≤1 page. |

---

## 3. Summary Table

| Action | Count | Items |
|---|---|---|
| **Remove** | 20 | All PHASE*/STEP* completion reports (14), CSCS/complex/UI-UX audit reports (3, optional archive), Elite deployment & enhancement summaries (2), settings summary (1) |
| **Merge → Remove** | 1 | `FORGE_SYSTEM_STATUS_REPORT.md` (fold into README) |
| **Move** | 1 | `docs/prompts/run/run_forge_demo.py` → scripts location |
| **Update** | 8 | README_FORGE_SYSTEM, FORGE_SYSTEM_VERIFICATION, GITHUB_PAGES_GUIDE, EXERCISE_LIBRARY_STATUS (or fold), EXERCISE_LIBRARY_COMPLETION_PLAN, LIBRARY_ENHANCEMENT_PLAN, forge_web UI/UX summary, forge_web mobile summary |
| **Create** | 8 | Root README, DATA_MODEL, MIGRATIONS, API_REFERENCE, CONTRIBUTING, TESTING, CHANGELOG, SECURITY |

---

## 4. Recommendations

- **R-1 — One fact, one home.** Counts, status, and architecture belong in exactly one document each (C-2, C-1, C-4). Every other doc links rather than restates. This is what prevented — and now must fix — the 271-vs-334-vs-537 contradiction.
- **R-2 — Stop phase-numbered reporting.** Future progress goes in `CHANGELOG.md` entries and PR descriptions. If a working plan is needed, keep numbered milestones only in issue trackers, not filenames.
- **R-3 — Doc hygiene rules going forward:** no first-person narrative, no emoji in headings, every dated claim carries an "as of" stamp, docs live in `docs/` (frontend-specific docs relocated), filenames in `UPPER_SNAKE.md` matching this audit's set.
- **R-4 — Conservative execution.** Create an `docs/archive/` folder if stakeholders want provenance for the removed audit reports; nothing else in the plan deletes information permanently except true duplicates (#5/#6).
- **R-5 — Out of scope (flagged, not acted on):** stray non-doc artifacts (`audit_report.json` ×2 locations, `exercises_data.py.tmp`, large JSON datasets, underscore-prefixed generator scripts in `tests/`). These are code/data-cleanup tasks for maintainers, referenced here only so they aren't mistaken for documentation.
