# Boundary-First Proof Modeling Spec Review R47

Review ID: spec-review-r47
Stage: spec-review
Round: 47
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: specs/rigorloop-workflow.md
Reviewed artifact: R28y runtime-projection candidate at 28338444
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR47-1
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Architecture assessment: architecture-required
Recording status: recorded
Review date: 2026-07-27
Context separation mechanism: separate-agent

Reviewed commit: `283384444fda941a9e2eda1fa46249a36eac089a`

Reviewed spec identity:
`sha256:f278f5d10a993b837a057ec90552fe11eb8c08148a9aca1800127c7bbcf84067`

## Result

Changes requested. R46's migration and routing gaps are closed, but the
non-exposure projection is not yet bound to the exact runtime implementation
that determines tool exposure.

## Material finding

### BFP-SR47-1 — The non-exposure projection is not bound to the runtime implementation that determines tool exposure

Finding ID: BFP-SR47-1

Severity: blocking

Evidence:

The projection selection key and complete projection row bind runtime version,
schema identity, protocol classification, and feature classification, but omit
the runtime package and launcher identities. A different runtime package could
therefore retain those declarations while changing tool-exposure behavior.
The effective-tool projection is feature-list-derived and is not an
independent runtime-owned inventory of every tool exposed to the model.

Required outcome:

Bind `not-exposed-projection` to the exact reviewed runtime implementation.

Safe resolution:

Add the exact runtime-package and launcher identities to the projection row
and selection key, recompute the canonical projection identity, bind all
values to the attestation, and add implementation-drift acceptance proof.

## Prior findings

- BFP-SR46-1: resolved.
- BFP-SR46-2: substantially resolved; implementation identity remains.
- BFP-SR46-3: substantially resolved; implementation identity remains.
- BFP-SR46-4: resolved.

## Readiness

Not ready for architecture. Resolve BFP-SR47-1 and rerun spec review.
