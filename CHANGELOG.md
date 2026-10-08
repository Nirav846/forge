# Changelog

All notable changes to FORGE are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning follows [SemVer](https://semver.org/).

> Note: this file replaces the retired per-phase completion reports (see
> `docs/DOCUMENTATION_AUDIT.md`). Add an entry per release or data migration —
> do not create new standalone "PHASE X COMPLETE" documents.

## [Unreleased]

### Added
- Documentation set from the 2026-09 documentation audit: root `README.md`,
  `docs/DATA_MODEL.md`, `docs/MIGRATIONS.md`, `docs/API_REFERENCE.md`,
  `docs/FRONTEND_UI_GUIDE.md`, `docs/TESTING.md`, `CONTRIBUTING.md`,
  `SECURITY.md`, and this changelog.

### Removed
- 17 obsolete phase/status completion reports and verification snapshots.
- 3 superseded audit reports archived to `docs/archive/`.

## Historical Baseline (reconstructed)

Exercise-library data migrations 000026–000035 expanded the library from ~40 to
the current frontend seed of **537 exercises / 222 complexes** (backend engine
data: 334), adding coaching cues, common faults, contraindications, development
levels, Olympic-lift framework fixes, unilateral/hip-dominant coverage,
conditioning protocols, and plyometrics. Details per migration: see
`migrations/` and `docs/DATA_MODEL.md`.
