# Contributing to FORGE

## Workflow

1. Branch from `main` (`feature/...`, `fix/...`, `docs/...`).
2. Make focused changes; add/extend tests (see `docs/TESTING.md`).
3. Open a pull request into `main`; keep PRs reviewable (< ~400 diff lines where practical).
4. Update `CHANGELOG.md` in the same PR for user-visible or data changes.
   Do not add new standalone status/completion reports — the changelog and PR
   description replace them (policy from `docs/DOCUMENTATION_AUDIT.md`).

## Environment Setup

```bash
# Backend
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn pytest          # plus any deps your change needs
python validate_forge_env.py                # confirm environment

# Frontend
cd forge_web && npm install
```

## Running Checks Before Requesting Review

```bash
pytest src/ tests/                          # backend suites
python test_complete_system.py              # end-to-end
python validate_library.py                  # if you touched exercise data
cd forge_web && npm run build && npm run test
```

Windows users can use `start_forge.bat` / `stop_forge.bat` to run the stack.

## Domain Data Changes

Adding or editing exercises/complexes must follow `docs/MIGRATIONS.md`
(schema, required coaching metadata, ID allocation, view regeneration).
Coaching content should cite authoritative S&C sources (NSCA/UKSCA/EXOS-style
references as used in existing migrations).

## Coding Conventions

- Python: PEP 8, type hints on public functions, no print-debug leftovers.
- TypeScript: strict mode; components colocated under `forge_web/src/`.
- Keep the offline-first principle: the console must degrade gracefully when the API is unreachable.

## Documentation Standards

- One fact, one home: link to the canonical doc instead of restating counts or status.
- Dated claims carry an "as of" stamp; neutral third-person tone; no emoji in headings.
- Docs live in `docs/` (root reserved for README/CHANGELOG/CONTRIBUTING/SECURITY).
