# FORGE Wave 10 — Stabilization Audit v1

## What Was Unstable at Start of Wave 10

### 1. Three Pre-Existing Test Failures

| Failure | Root Cause | Disposition |
|---------|------------|-------------|
| `test_intent_categories_cover_all_families` | `Landing` family existed in `FamilyCode` enum but was not listed in `INTENT_CATEGORIES` in `data.py`. Cross-family substitution and intent mapping could not find Landing exercises. | Fixed — added `"Landing"` to `"explosive"` intent category |
| `test_ut11_training_age_4_advanced` | Test used default `age=18` (from `AthleteProfile` default), triggering youth capping `cap = (18-14)*0.5 = 2` — reducing 4yr training to 2yr effective → INTERMEDIATE instead of ADVANCED | Fixed — updated test to set `age=23`. Added new test `test_ut11d_youth_cap_prevents_advanced` to explicitly verify youth cap works |
| `test_default_personalization_notes_empty` | Test expected `[]` personalization_notes, but Wave 8 role-week-profiling generates 4 baseline notes for any default rugby profile (collision robustness, rotational exposure, conditioning density, eccentric tolerance) | Fixed — renamed to `test_default_personalization_notes_baseline`, expects non-empty notes with role mention |

### 2. API/Frontend Integration Weak Points Found

| Weak Point | Severity | Resolution |
|------------|----------|------------|
| No PATCH endpoint for partial artifact updates | Medium | Added `PATCH /api/programs/{id}` — supports status, coach_notes, internal_notes updates without round-tripping full payload |
| No schema version on artifacts | Medium | Added `schema_version: 1` to artifact structure, exposed in list view, documented in schema spec |
| Update_artifact had no allowed-fields filter | Low | Added whitelist to prevent accidental field writes |
| List view didn't surface schema_version | Low | Added schema_version to list summary |
| Malformed artifact file could crash list view | Low | Already handled (try/except around JSON parse) — verified in tests |

### 3. Save/Load Artifact Risks Found

| Risk | Status | Mitigation |
|------|--------|------------|
| No schema version → future format changes break old artifacts | Fixed | `schema_version` field added. Old artifacts without it load gracefully (field absent) |
| No partial update endpoint → saving reviewed status requires full payload round-trip | Fixed | `PATCH` endpoint added with whitelisted fields |
| Coach notes lost on duplicate | Verified | Duplicate clears coach_notes — documented behavior |
| Malformed JSON in artifact dir | Verified | Silently skipped in list view |
| Artifact directory doesn't exist | Verified | Auto-created in `_ensure_dir()` |

### 4. Remaining Non-Blocking Risks

1. **Weekly exposure placeholders**: `exposure_summary` fields still show `"Not specified"`. Serializer enrichment would require calling `program_exposure_summary()` and wiring results through contract - ~20 line change, deferred post-launch.

2. **Dropped constraints empty**: `dropped_constraints: []` in every response. Backend drops constraints but doesn't surface them. Requires serializer change to collect from `program_adjustments` / role-slot logic.

3. **No server-side PDF**: Browser print is sufficient for controlled testing but may produce coarser output than coaches expect for client delivery.

4. **Exercise swap/edit not persisted**: UI edits remain in-browser state. Requires frontend-side override model + save mechanism.

5. **Coach notes not editor-backed**: PATCH endpoint exists now, but frontend notes editor isn't wired to call it.

6. **Manual E2E not recorded**: All QA flows are defined in the UAT pack but not yet executed by a human tester against a running system.
