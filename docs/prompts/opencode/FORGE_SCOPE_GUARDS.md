# FORGE SCOPE GUARDS — DRIFT PREVENTION LAYER

## Allowed Work
- frontend UI changes directly tied to coach workflow
- backend PATCH / persistence updates
- artifact schema extensions (minimal)
- compare + library improvements
- validation + UX reliability improvements

---

## Forbidden Work
- building analytics dashboards
- building AI summarizers
- rewriting engine architecture
- introducing event-driven systems
- building new data pipelines
- creating standalone tools/scripts unrelated to workflow

---

## Red Flag Behaviors (STOP if these appear)
If the system starts:
- creating “helper tools”
- building “insight engines”
- adding “audit layers”
- designing “future extensibility”

→ immediately reduce scope to current requirement only.

---

## Hard Rule
If a feature does not directly change coach interaction with:
- program creation
- program editing
- program saving
- program comparison

→ it is out of scope.