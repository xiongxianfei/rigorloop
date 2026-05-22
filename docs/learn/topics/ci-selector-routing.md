# CI Selector Routing

This topic is curated learn guidance. Authoritative CI behavior remains in accepted specs, active plans, selector code, test specs, and validation scripts.

## 2026-05-22: New Change-Local Evidence Classes Need Deterministic Selector Routes

- Source session: `docs/learn/sessions/2026-05-22-change-local-selector-routing.md`
- Primary classification: `durable-lesson`
- Secondary routes: current selector fix remains CI-maintenance for the active broad-smoke output-compaction change; possible later workflow checklist update

RigorLoop allows useful change-specific proof artifacts under `docs/changes/<change-id>/`, but the v1 validation selector is intentionally deterministic. A changed path must map to a known validation category and check set. When a change invents a new evidence filename without adding selector routing and regression coverage, local or PR CI can block with `manual-routing-required` even though the evidence file is valid and useful.

Root rule:

```text
Adding a new change-local evidence artifact class also adds a selector-routing obligation.
```

Best practice:

- classify each new `docs/changes/<change-id>/...` evidence filename when it is introduced;
- route deterministic lifecycle evidence to `artifact_lifecycle.validate` or another specific check;
- add regression coverage in `scripts/test-select-validation.py`;
- prefer bounded filename patterns for recurring evidence classes over one-off exact names;
- treat `manual-routing-required` as a final-readiness blocker for deterministic in-repo evidence.

Explicit lifecycle validation over known paths is not enough. It proves the artifact content, but it does not prove that local or PR CI can route the complete changed-path set.
