# Testing Map

**Purpose:** Locate the right test suite and how to run it. The repo's test
assets are fragmented across three areas; this page is the index until they are
consolidated. As of 2026-09-24.

## How to Run

```bash
pytest src/                 # engine module unit tests
pytest tests/               # feature "wave" suites
python test_complete_system.py   # end-to-end system check
python validation_test.py        # data validation flows
cd forge_web && npm run test     # frontend (vitest)
```

## Backend Engine Tests (`src/test_*.py`)

| File | Scope |
|---|---|
| `test_assessment_entry.py` | Assessment entry module |
| `test_athlete_module.py`, `test_athlete_intelligence_layers.py` | Athlete profiles & intelligence layers |
| `test_deficit_engine.py`, `test_demand_scoring_engine.py` | Deficit detection, demand scoring |
| `test_program_builder.py`, `test_session_generator.py` | Program/session generation |
| `test_exercise_substitution.py` | Substitution engine |
| `test_integration_workflow.py`, `test_e2e_integration.py` | Cross-module integration |
| `test_recommendation_observability.py` | Recommendation logging |
| `test_wave1_hardening.py`, `test_wave2_prescription.py` | Hardening/prescription waves |

## Feature Waves (`tests/`)

| File | Scope |
|---|---|
| `test_competition_aware.py`, `test_conditioning.py`, `test_generator.py` | Core behaviors |
| `test_hardening_phase.py`, `test_warmup_hardening.py`, `test_warmup_recovery.py` | Robustness |
| `test_movement_slot_layer.py` | Movement-slot programming |
| `test_wave3_progression.py` … `test_wave11a_*.py` | Progression, periodization, personalization, autoregulation, block/role-week planning, session assembly |
| Files prefixed `_` (e.g., `_generate_wave7_tests*.py`) | **Deprecated test generators**, not tests — do not run; cleanup candidates |

## API Tests

| File | Scope |
|---|---|
| `src/forge/test_api_integration.py` | FastAPI endpoint integration |
| `src/forge/test_adjustment_engine.py` | Adjustment logic |
| `_test_api_server.py`, `_test_serializer.py` (root) | Underscore-prefixed scratch tests — deprecated; port needed cases into `src/forge/test_api_integration.py` |

## Data Validation

| Command | Purpose |
|---|---|
| `python validate_library.py` | Exercise record schema/completeness checks |
| `python scripts/audit_500.py` / `analyze_500.py` | Library coverage audits |
| `python smoke_check_forge.py`, `python validate_forge_env.py` | Environment & smoke checks |

## Conventions

- New tests go next to the module they cover (`src/.../test_*.py`) or in `tests/`
  for cross-cutting features. No underscore-prefixed "test" files.
- Every migration PR includes a `validate_library.py` run; every API PR extends
  `test_api_integration.py`.
