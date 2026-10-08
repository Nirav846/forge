# Database Migration Workflow

**Purpose:** How to add or modify exercise-library and application data safely.

## Conventions

- Tool: golang-migrate style pairs: `NNNNNN_description.up.sql` / `.down.sql` in `migrations/`.
- Current version: **000035** (`000035_conditioning_plyometrics`). New files take the next number.
- Every `up` migration MUST have a working `down` migration that fully reverses it.
- Seed inserts should be idempotent where possible (`INSERT ... ON CONFLICT DO NOTHING`).
- Never reuse or edit exercise IDs from earlier migrations; allocate new IDs after
  the current max. (Historical defect: overlapping ID ranges between the retired
  "Phase" reports and migrations 000026–000035 caused duplicate/conflicting entries.)
- `PHASE_5A_SEED.sql` is a legacy standalone file; do not follow its pattern — use numbered pairs.

## Adding Exercises — Checklist

1. Draft rows against the schema documented in `DATA_MODEL.md`
   (tables: `exercises`, `exercise_tags`, `exercise_movement_patterns`,
   `exercise_equipment`, `exercise_sport_mapping`, `exercise_physical_qualities`,
   `exercise_training_methods`).
2. Required coaching metadata per record: 4 `coaching_cues`, 4 `common_faults`,
   contraindications/pain-safe flags, development level, technical difficulty.
3. Classify movement pattern and equipment using the existing taxonomy — no new
   category strings without updating `forge_web/src/data/exerciseOrganization.ts`.
4. Write `up` + `down`, apply to a scratch SQLite DB, and run
   `python validate_library.py` plus `python scripts/audit_500.py` for gap analysis.
5. Regenerate downstream views: `python dump_exercises.py` → refresh
   `forge_web/src/data/exercises.json` (and engine data if applicable).
6. Add a `CHANGELOG.md` entry with the migration ID and count delta.

## Applying Migrations

```bash
# Example using the migrate CLI against the local SQLite file:
migrate -path migrations -database "sqlite3://forge.db" up
migrate -path migrations -database "sqlite3://forge.db" down 1   # rollback last
```

If the migrate CLI is unavailable, document the manual application steps in the PR.
