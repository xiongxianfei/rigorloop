# Boundary-First Proof Model Spec Review R3

Review ID: spec-review-r3
Stage: spec-review
Round: 3
Reviewer: Independent contract rereview
Target: specs/boundary-first-proof-model.md
Status: changes-requested
Material findings: PBF-SR4, PBF-SR5, PBF-SR6, PBF-SR7, PBF-SR8
Architecture assessment: required after spec revision
Immediate next stage: spec revision
Eventual test-spec readiness: not-ready

## Result

The revision correctly removes repository rollback state, activation and
rollback writers, transaction receipts, and attestation stores. It preserves
historical artifacts and the structural-versus-semantic ownership boundary.

Five activation and rollback details remain ambiguous and prevent
deterministic testing.

## Findings

## Finding PBF-SR4

Finding ID: PBF-SR4
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R003 and PBF-R053

Evidence: PBF-R003 forbids the marker while activation is pending, but PBF-R053
permits in-flight opt-in without limiting it to active state or defining a
pending exception.

Required outcome: define whether in-flight opt-in is active-only or a bounded
pending-state exception.
Safe resolution path: Make in-flight opt-in active-only.
needs-decision rationale: none

## Finding PBF-SR5

Finding ID: PBF-SR5
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R005a and Observability

Evidence: PBF-R005a and Observability require an activating release only "when
known," while the acceptance criteria claim deterministic release evidence.

Required outcome: define the release-identity field for both pending and active
states, requiring an immutable identity in active state.
Safe resolution path: Require `-` while pending and an immutable identifier
while active.
needs-decision rationale: none

## Finding PBF-SR6

Finding ID: PBF-SR6
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R005a and PBF-R049b

Evidence: PBF-R005a requires sorted grandfathered paths and PBF-R049b relies on
them without defining eligibility, path grammar, exclusions, or capture time.

Required outcome: define the exact membership and sorting rules.
Safe resolution path: Define activation-time eligibility, path grammar,
exclusions, and bytewise sorting.
needs-decision rationale: none

## Finding PBF-SR7

Finding ID: PBF-SR7
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R057 and PBF-R058

Evidence: PBF-R057 and PBF-R058 do not define the target release, release
metadata owner, per-adapter identity set, resulting capability state, or
missing and mixed-package behavior.

Required outcome: define a deterministic rollback target and ordinary release
metadata evidence without adding an attestation store.
Safe resolution path: Select the immediately preceding release and validate
its complete supported-adapter package identity matrix from ordinary release
metadata.
needs-decision rationale: none

## Finding PBF-SR8

Finding ID: PBF-SR8
Severity: major
Location: specs/boundary-first-proof-model.md, PBF-R057 and Non-goals

Evidence: PBF-R057 requires installation or republication while the non-goals
exclude external publication and mutation.

Required outcome: separate read-only rollback validation from operator-owned
external execution.
Safe resolution path: Keep selection and package validation in scope and leave
external installation or publication to an authorized release operator.
needs-decision rationale: none

## Review Dimensions

| Review dimension | Verdict |
| --- | --- |
| requirement clarity | block |
| normative language | block |
| completeness | block |
| testability | block |
| examples | concern |
| compatibility | block |
| observability | block |
| security/privacy | pass |
| non-goals | block |
| acceptance criteria | block |

## Recommendation

Revise the activation and rollback clauses only. Keep the simplified
published-skill boundary and do not restore writer, receipt, transaction, or
attestation machinery.
