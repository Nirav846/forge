# FORGE Coach Console — Frontend UI Guide

**Purpose:** Durable reference for the exercise-library UI and responsive design
conventions of `forge_web/` (React 18 + TypeScript + Vite + Tailwind).
Consolidates and replaces the former implementation summaries
(`forge_web/UI_UX_IMPLEMENTATION_SUMMARY.md`,
`forge_web/mobile_responsive_summary.md`). As of 2026-09-24.

## Library Organization

The flat ~22-category list is replaced by a hierarchical taxonomy defined in
`src/data/exerciseOrganization.ts`:

- **7 super-categories** group all library categories for navigation.
- Each category maps to exactly one super-category; new categories must be
  registered there before use (see `MIGRATIONS.md` checklist step 3).
- Category configuration lives in `src/modules/exercises/ExerciseLibrary.tsx`
  (`CATEGORY_GROUPS`); keep it in sync with `exerciseOrganization.ts`.

## Exercise Detail Modal — Data Contract

The modal renders these fields when present and degrades gracefully when absent:

| Section | Field(s) | Fallback behavior |
|---|---|---|
| Coaching cues | `coaching_cues` | Hide section if empty |
| Common faults | `common_faults` | Hide section if empty |
| Safety | contraindications / pain-safe flags | Show warning styling only when flagged |
| Classification | movement pattern, equipment, development level | Show "Unclassified" badge |
| Actions | add-to-workout / substitute | Always visible |

Visual hierarchy: name & media → prescription defaults → cues/faults → safety →
metadata. Do not reorder without a UX review.

## Filtering & Search

- Faceted filters: super-category, category, equipment, movement pattern,
  development level, pain-safe toggle.
- Text search hits names, aliases, and coaching cues via `/api/v1/exercises/search`
  (online) or the local JSON seed (offline-first mode).
- View modes: Grid and List toggles persist per session.

## Responsive Design Conventions

- Mobile-first; Tailwind breakpoints (`sm 640 / md 768 / lg 1024 / xl 1280`).
- Header collapses to hamburger nav below `md`; primary actions move into the
  mobile menu bar.
- Library grid density: 1 column (mobile) → 2 (`sm`) → 3 (`lg`) → 4 (`xl`).
- Touch targets ≥ 44 px; modals render full-screen below `sm`.
- Home screen ("Command Center") stacks hero → quick stats → tool cards on mobile.

## Settings

Theme switching and preferences are managed by the Settings modal
(`src/components/Settings/SettingsModal.tsx`); preferences persist locally
(offline-first principle — no server round-trip required).

## Quality Gates

- `npm run build` must pass type-checking (`tsconfig.json`, strict).
- Component tests run under vitest (`vitest.config.ts`).
- Deployment builds as a static site; the Vite `base` path must match the
  GitHub Pages route (see `GITHUB_PAGES_GUIDE.md`).
