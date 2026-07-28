# Boundary-First Execution Plan Review R2

Review ID: plan-review-r2
Stage: plan-review
Round: 2
Reviewer: Independent plan reviewer
Target: docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md
Status: changes-requested
Material findings: PBF-PLR1, PBF-PLR2, PBF-PLR3
Immediate next stage: plan revision
Test-spec readiness: not-ready

## Finding PBF-PLR1

Finding ID: PBF-PLR1
Severity: major
Location: Governing artifacts
Evidence: The plan names only the superseded activation ADR and omits its
accepted replacement.
Required outcome: make the replacement ADR the current governing decision.
Safe resolution path: replace the stale ADR link.
needs-decision rationale: none

## Finding PBF-PLR2

Finding ID: PBF-PLR2
Severity: major
Location: M3, M4, and Sequencing and proof timing
Evidence: M3 and M4 duplicate rollback-readiness proof, while no sequencing row
or exact M4 integration command proves active-manifest selection against real
release metadata and the current adapter inventory.
Required outcome: assign fixture/schema logic to M3 and real metadata
integration to M4 with an explicit proof row and command.
Safe resolution path: narrow M3, add one existing-validator M4 invocation over
an active fixture, and add the proof-timing row.
needs-decision rationale: none

## Finding PBF-PLR3

Finding ID: PBF-PLR3
Severity: major
Location: M4 recovery and commit identity
Evidence: M4 forbids external release action and remains pending, but recovery
requests package reinstallation and the commit identity claims activation.
Required outcome: keep recovery repository-local and name the milestone as
release readiness.
Safe resolution path: retain or restore pending manifest bytes and rename the
commit identity.
needs-decision rationale: none

## Recommendation

Correct the three bounded planning defects and repeat plan review.
