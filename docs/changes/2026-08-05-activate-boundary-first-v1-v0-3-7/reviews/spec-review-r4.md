# Specification Review R4

Review ID: spec-review-r4
Stage: spec-review
Round: 4
Reviewer: independent Codex spec-review peer
Target: `specs/boundary-first-v1-v0-3-7-activation-release.md`
Target revision: `ee28ad638270b4041971d232c221f46e85e99aff`
Status: changes-requested
Material findings: BFA-SR4-001
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready
Automatic downstream handoff: workflow-owned after recording and resolution

## Result

- `BFA-SR3-001`: resolved for its post-tag authority requirement; a narrower
  composition inconsistency is recorded as `BFA-SR4-001`.
- `BFA-SR3-002`: resolved.
- Architecture handoff: blocked until phase-description consistency is corrected.
- Recording status: recorded
- Recording blocker: none

R018 now defines a realizable post-local-tag publication-readiness gate and
separates stored `R/C` provenance from freshly derived `H`. One composition
description still contradicts that contract.

## Material Finding

### Finding BFA-SR4-001

Finding ID: BFA-SR4-001
Severity: major
Status: failed-remediation
Location: E3; BND-COMPOSE-001; INT-004
Evidence: E3 places both strict validation and full release verification at
tagged tree `T`, while R018 and R019 place ordinary strict validation and
publication readiness at live `H` and only full release verification at `T`.
BND-COMPOSE-001 and INT-004 also omit the distinct publication-readiness gate.
Required outcome: Express all three pre-publication gates consistently:
ordinary strict validation at `H`, publication readiness at `H`, and full
release verification from tagged tree `T`.
Safe resolution path: Rewrite E3 and add publication readiness to
BND-COMPOSE-001 and INT-004 without expanding the scenario inventory.
needs-decision rationale: none; R018 already fixes the governing phase order.

## Finding Reconciliation

| Finding | R4 result | Requirement mapping |
| --- | --- | --- |
| BFA-SR3-001 | resolved | Glossary, R016 through R018, EC11A, and AC-BFA-007 now define the phase correctly. |
| BFA-SR4-001 | open | E3, BND-COMPOSE-001, and INT-004 require alignment with that phase. |
| BFA-SR3-002 | resolved | Identity applicability includes R017; BND-AUTH-001, INT-002, and E4 own the corrected provenance. |

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | concern |
| normative language | pass |
| completeness | concern |
| testability | block |
| examples | block |
| compatibility | pass |
| observability | pass |
| security/privacy | pass |
| non-goals | pass |
| acceptance criteria | pass |

## Validation Evidence

- `python scripts/validate-boundary-first.py --path specs/boundary-first-v1-v0-3-7-activation-release.md` passed.
- `git diff --check e756a6d67263ef7e7df42ae288f1090fcf77476a..ee28ad638270b4041971d232c221f46e85e99aff -- specs/boundary-first-v1-v0-3-7-activation-release.md` passed.

## Recommendation

Align the three existing composition descriptions, then perform spec-review R5.
