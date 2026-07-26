# Boundary-First Proof Modeling Spec Review R43

Review ID: spec-review-r43
Stage: spec-review
Round: 43
Reviewer: Codex spec-review skill with context-separated independent reviewer
Target: read-only transport proof candidate at 126140b9
Reviewed artifact: specs/rigorloop-workflow.md
Status: changes-requested
Review status: changes-requested
Material findings: BFP-SR43-1, BFP-SR43-2, BFP-SR43-3
Immediate next stage: spec
Architecture assessment: architecture-required
Test-spec readiness: not-ready
Recording status: recorded
Review date: 2026-07-26
Context separation mechanism: separate-agent

Reviewed spec identity: `sha256:cd1db59f123ab79bcffc79295e0c4cd805ec6b47d8cf756764299c90af23d65e`

## Result

The typed preflight and generation-start baseline-failure surfaces resolve the
observability gap in BFP-SR42-2. Three contract gaps remain: the probe's
decline rule does not govern accepted turns, the expanded exact attestation
shape retains its old schema version, and the fixed failure record declares an
unreachable size boundary without a legal overflow result.

## Material findings

### BFP-SR43-1 — The probe does not bind file-change denial to accepted turns

Finding ID: BFP-SR43-1

Severity: blocking

Location: workflow spec file-change denial probe and accepted-turn contract

Evidence:

The probe accepts generic `failed`, which has no machine-readable denial cause
in the pinned runtime schema. Its exact `decision: decline` rule applies only
to the probe, so canary, accepted stage, retry, or reconciliation turns could
still receive `accept` or `acceptForSession`.

Required outcome:

Bind one identity-bound deny policy to the probe and every governed turn, and
prove denial through an approval request followed by `decline` and a terminal
`declined` file-change item.

Safe resolution:

Remove generic `failed` as proof, forbid every accept decision, bind the shared
policy through configuration, attestation, canary, generation, retry, and
validation, enumerate the generic item carriers, and make the parent-created
fixture directory and initial absence state explicit.

### BFP-SR43-2 — Runtime attestation v1 is mutated in place

Finding ID: BFP-SR43-2

Severity: major

Location: workflow spec exact runtime-attestation record

Evidence:

The exact record adds a file-change policy identity and probe result while
retaining `boundary-runtime-attestation-v1`, giving one version two
incompatible shapes.

Required outcome:

Give the expanded shape a new version and deterministic treatment for old
evidence.

Safe resolution:

Use `boundary-runtime-attestation-v2` for new preflight and generation
evidence, keep v1 historical/readable but stale for the new boundary, and bind
v2 through manifests, input identities, immutable runs, pointers, validation,
and reporting.

### BFP-SR43-3 — The workspace-failure size boundary is unreachable

Finding ID: BFP-SR43-3

Severity: major

Location: workflow spec workspace-baseline failure result

Evidence:

Every valid fixed-shape record is 248–271 canonical bytes. No valid record can
reach or exceed 1024 bytes, and the spec defines no legal replacement result
if the adapter nevertheless classifies its own record as oversized.

Required outcome:

Use a reachable boundary or rely on the intrinsic bound of the exact closed
schema while keeping every failure result legal.

Safe resolution:

Remove the arbitrary numeric runtime limit. State that the fixed fields,
fixed-length identities, and closed reason vocabulary intrinsically bound the
record; reject unknown reasons and additional fields.

## Review dimensions

| Dimension | Result |
| --- | --- |
| Requirement clarity | block |
| Normative language | concern |
| Completeness | block |
| Testability | block |
| Compatibility | block |
| Observability | block |
| Security and privacy | block |
| Non-goals | pass |
| Acceptance criteria | concern |

## Readiness

Not ready for architecture or test-spec reliance. Resolve BFP-SR43-1,
BFP-SR43-2, and BFP-SR43-3 and obtain an approved spec rereview.
