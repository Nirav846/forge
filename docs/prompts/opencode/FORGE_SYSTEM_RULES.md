# FORGE SYSTEM RULES — HARD CONSTRAINT LAYER

These rules apply to all OpenCode / AI runs inside FORGE.

## 1. Primary Objective Priority
Always prioritize:
1. Real coach workflow behavior
2. Artifact correctness and persistence
3. Deterministic program structure
4. Minimal viable implementation

Never prioritize:
- refactoring for aesthetics
- speculative architecture changes
- non-functional abstractions

---

## 2. No Speculative Engineering
Do not introduce:
- new systems unless explicitly required
- new frameworks
- new database layers
- new services

If a requirement can be solved by extending current structures, do that.

---

## 3. Artifact Integrity Rule
All program outputs must be:
- reproducible
- reload-safe
- override-safe

Coach overrides must NEVER mutate core engine output destructively.

---

## 4. Minimal Change Principle
When implementing features:
- change the smallest number of files possible
- prefer extension over rewrite
- prefer additive schema changes over restructuring

---

## 5. Coach Reality Test
Every feature must answer:
"Would a real S&C coach actually use this daily?"

If no → it is not required.

---

## 6. Output Discipline
AI must not generate:
- analysis scripts unless explicitly required
- documentation unrelated to implementation
- generalized system redesigns

Only implement what is asked in scope.