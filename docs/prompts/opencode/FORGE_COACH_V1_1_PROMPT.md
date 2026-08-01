# FORGE Coach Console v1.1 — Real Coach Workflow Pass

(Use alongside SYSTEM_RULES + SCOPE_GUARDS + MASTER_RUNNER)

You are working inside the FORGE repository.

Your job is to implement the next frontend pass for the Coach Console.

---

## Objective
Transform the Coach Console from a generator shell into a real coaching workflow tool.

---

## Hard Scope (ONLY THESE 5 AREAS)

1. Builder interactions → real persistent overrides
2. Library → search, filter, sort, scan usability
3. Compare → meaningful coaching diff
4. Form validation → safe input + UX feedback
5. Save/review → real API-driven state

---

## Non-negotiable constraints
- No architecture rewrites
- No new systems
- No analytics tools
- No speculative features
- No “future-proofing”

---

## Artifact Rule
All coach edits must persist via:
- explicit override layer
- PATCH-based persistence
- reload-safe structure

Do not mutate core engine output.

---

## Compare Requirement
Must show:
- session differences
- exercise swaps
- prescription changes
- weekly structure changes
- coach override visibility

---

## Library Requirement
Must include:
- search (athlete name)
- filter (sport, status)
- sort (updated, name)

Must improve scanability.

---

## Validation Requirement
Must block invalid submission.
Must show inline errors.
Must not allow silent failures.

---

## Save/Review Requirement
Must reflect real API state.
No fake “saved” UI states.

---

## Output
Provide:
- changed files
- backend changes
- schema changes
- verification checklist
- remaining gaps

No extra artifacts.