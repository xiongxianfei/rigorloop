# Architecture Progressive-Guidance Revision Evidence

- Artifact ID: `architecture`
- Artifact path: `docs/architecture/system/architecture.md`
- Authoring stage: `architecture`
- Completion status: `complete`
- Resulting review-request path: `docs/changes/2026-07-28-stage-owned-lifecycle-artifacts-and-change-local-workflow-state/reviews/architecture-review-r5.md`

## Revision result

The canonical architecture now includes the progressive boundary-first
guidance design approved by the progressive-guidance proposal, specification,
and ADR. The revision covers resource ownership and projection, compact versus
expanded guidance, stage-family consumption, selector behavior, generated and
installed parity, activation, rollback, and verification boundaries.

This record restores the canonical architecture to its established owning
change record. The progressive-guidance change remains the source of the
feature requirements and implementation evidence, but it does not create a
second mutable lifecycle owner for the shared canonical architecture.

## Review target

Architecture review R3 must inspect the complete current architecture package,
including the progressive-guidance sections and their alignment with:

- `specs/progressive-boundary-first-skill-guidance.md`;
- `docs/adr/ADR-20260729-progressive-boundary-guidance-resources.md`;
- `specs/stage-owned-lifecycle-artifacts-and-change-local-workflow-state.md`;
- the existing C4 diagram sources under
  `docs/architecture/system/diagrams/`; and
- the single-owner lifecycle contract represented by this change record.

Architecture-review R3 requested resolution of `AR3-001`, `AR3-002`, and
`AR3-003`, plus one minor schema-label correction. Authoring is reopened for
those exact corrections; architecture-review R4 is the resulting review target.

The revision aligns architecture-method R8, its proof wording, the template,
and published architecture skills with stable owner metadata; updates active
ADR wording; distinguishes owner-family initial loading from downstream
expansion loading; and corrects the schema-v3 container label.

Architecture-review R4 reopens authoring for `AR4-001` and `AR4-002`: four
stale supersession summaries and the remaining schema-v2 current-write
descriptions. No ADR body changes.

The four historical automation ADR summaries now use current superseded
classification. The CLI goal, white-box serializer responsibility, and quality
scenario now identify schema v3 as the current write format and schemas v1/v2
as compatibility inputs.
