# Architecture Method Supporting Spec Review R1

Review ID: spec-review-architecture-method-r1
Stage: spec-review
Round: 1
Reviewer: independent Codex spec-review peer
Target: specs/architecture-package-method.md
Reviewed artifact: specs/architecture-package-method.md
Review date: 2026-08-02
Status: approved
Recording status: recorded
Material findings: APM-SR1-001 (resolved)
Immediate next stage: architecture
Eventual test-spec readiness: ready
Automatic downstream handoff: none

## Result

R8 is a coherent, narrow correction for canonical `architecture.md`, but the
same active lifecycle contract still conflicts with the ADR requirements,
template, proof map, review checklist, acceptance criterion, and observability
wording.

## Material finding

### APM-SR1-001 - ADR lifecycle ownership remains contradictory

Finding ID: APM-SR1-001
Severity: blocking
Location: specs/architecture-package-method.md R46-R48 and AC7; templates/adr.md; skills/architecture-review/SKILL.md; specs/architecture-package-method.test.md T7
Evidence: SLA-R002 makes the stage-owned lifecycle spec the sole normative owner of governed artifact-state placement and SLA-R014 prohibits mutable lifecycle status in governed artifacts. R46-R47, the ADR template, architecture-review checklist, T7, AC7, and observability wording still require or describe embedded ADR status.
Required outcome: Complete the same stable-pointer and change-local mutable-state correction for newly governed ADRs while preserving explicit compatibility for unmigrated historical ADRs.
Safe resolution path: Amend R46-R48, AC7, observability, the ADR template, architecture-review checklist, and T7 consistently. Existing unmigrated ADRs remain historical and are not mass-rewritten.

## Review dimensions

R8 clarity and scope pass. Normative consistency, completeness, testability,
compatibility, observability, and acceptance criteria are blocked by
`APM-SR1-001`. No owner decision is required because the higher-ranked active
lifecycle contract already determines the outcome.

## Rereview

`APM-SR1-001` is resolved. R46-R48, AC7, observability, templates,
architecture skills, and T7 now consistently require stable owner pointers
and exact change-local state for new governed artifacts while preserving
unmigrated historical compatibility. All review dimensions pass.

## Recommendation

Approved. Settle only `spec-architecture-package-method` to `approved` and
preserve workflow routing.
