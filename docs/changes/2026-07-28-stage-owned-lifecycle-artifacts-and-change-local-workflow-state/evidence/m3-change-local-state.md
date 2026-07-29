# M3 Change-Local State Evidence

Stage: implement
Milestone: M3
Result: passed

The existing change-metadata validator now recognizes the prospective
`stage-owned-change-local-v1` record, validates closed artifact, review,
workflow, blocker, milestone, and automation vocabularies before consistency,
and rejects duplicate paths, mixed writers, malformed evidence paths, and
illegal artifact transitions.

The existing automation-state module now exposes a bounded stage-owned store.
Reads are side-effect free; replacement is complete-file, validated,
optimistically locked, and atomic.

Commands:

- `python scripts/test-change-metadata-validator.py` — 60 passed.
- `python scripts/test-workflow-automation-state.py` — 64 passed.
- `python scripts/validate-change-metadata.py
  docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/change.yaml`
  — passed under historical compatibility.

No hash-based document contract, selector, protected-path rule, policy
registry, write interceptor, or new validator family was introduced.
