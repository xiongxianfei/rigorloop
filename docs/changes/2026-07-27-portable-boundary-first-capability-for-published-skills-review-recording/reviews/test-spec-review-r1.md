# Boundary-First Proof Model Test Spec Review R1

Review ID: test-spec-review-r1
Stage: test-spec-review
Round: 1
Reviewer: Codex test-spec-review
Target: specs/boundary-first-proof-model.test.md
Reviewed artifact: specs/boundary-first-proof-model.test.md
Review date: 2026-07-28
Recording status: recorded
Status: changes-requested
Review status: changes-requested
Material findings: PBF-TSR1, PBF-TSR2
Immediate next stage: review-resolution
Implementation handoff: not-allowed
Automatic downstream handoff: none

## Result

- Skill: test-spec-review
- Review status: changes-requested
- Material findings: PBF-TSR1, PBF-TSR2
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/reviews/test-spec-review-r1.md
- Review log: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-log.md
- Review resolution: docs/changes/2026-07-27-portable-boundary-first-capability-for-published-skills-review-recording/review-resolution.md
- Open blockers: normative and acceptance-criterion traceability is incomplete; broad-smoke ownership conflicts with its first required gate
- Immediate next stage: review-resolution
- Implementation handoff: not-allowed
- Stop condition: revise and rereview the active test spec before M1 implementation

## Review inputs

| Artifact | SHA-256 |
| --- | --- |
| `specs/boundary-first-proof-model.test.md` | `c06221adfc63d1e1e47d06efa77130b62aec61cad280c7967e0fd37e9892f717` |
| `specs/boundary-first-proof-model.md` | `d56e3ce553f2970f7ac872f7d4372bd24d138de8617dba240190f9dbd378e16b` |
| `docs/plans/2026-07-27-portable-boundary-first-capability-for-published-skills.md` | `de19115ade81fbc3d8ed4a84be57a78b742d9f550dbedfd8093b5ff86eed4f91` |
| `docs/architecture/system/architecture.md` | `176721282860df20ea71eb403c20bf725e86a99d90092ecc42c9605622066325` |
| `docs/adr/ADR-20260727-portable-boundary-first-reference-projection-and-activation.md` | `030caf8fe3920810b603d53c3b449b1caeb81c676a8ed336a1e93af769503740` |

The feature spec, architecture, ADR, and plan are approved, plan-review R1 is approved, and upstream material findings are closed. The proof map is therefore reviewable; both findings are local to the test specification.

## Findings

### PBF-TSR1

Finding ID: PBF-TSR1
Severity: major
Location: `specs/boundary-first-proof-model.test.md:55-72` and `specs/boundary-first-proof-model.test.md:376-399`
Evidence: The requirement map covers numbered PBF requirements and companion-spec ranges, but it has no acceptance-criterion map for PBF-AC001 through PBF-AC014. Normative observability, privacy, accessible Markdown, and no-network/no-Cartesian-product obligations outside the numbered requirement block appear only as prose in later verification sections; they do not cite stable test IDs, commands, milestones, or failure meaning. AGENTS.md requires every feature-spec `MUST` to map to a test.
Required outcome: Map every acceptance criterion and every normative obligation outside the numbered requirement block to stable test IDs and executable command ownership. Add or refine test cases where the existing tests do not directly prove diagnostic fields, redacted evidence, readable published Markdown, or the ordinary-authoring no-network/no-Cartesian-product boundary.
Safe resolution path: Add acceptance-criterion and supplemental normative-coverage tables. Extend T5, T11, T14, and T15 where they already own the behavior, and add one focused evidence-safety/accessibility test only if those existing cases cannot express direct proof. Bind all additions to the existing M2 through M4 commands and milestones without expanding product scope.
needs-decision rationale: none

### PBF-TSR2

Finding ID: PBF-TSR2
Severity: major
Location: `specs/boundary-first-proof-model.test.md:116` and `specs/boundary-first-proof-model.test.md:128`
Evidence: CMD13 assigns broad smoke to owner `verify`, but marks it first required at `code-review M4` and includes it in M4's pre-review proof row. An implementation milestone cannot satisfy a pre-code-review gate through authority owned only by the later final-verify stage.
Required outcome: Give the pre-code-review broad-smoke run an implementation-stage owner and retain an independently owned final-verify rerun, with unambiguous command IDs and first-required gates.
Safe resolution path: Split the repeated broad-smoke invocation into two command records. Assign the M4 run to `implement` with first gate `code-review M4`, assign the final rerun to `verify` with first gate `verify`, and update the M4 proof map plus performance text to cite both IDs.
needs-decision rationale: none

## Review dimensions

| Dimension | Verdict | Notes |
| --- | --- | --- |
| Governing-contract alignment | pass | The proposed proof behavior follows the approved contract, architecture, and plan. |
| Requirement coverage | block | Numbered requirements are mapped, but unnumbered normative obligations are not directly traceable. |
| Example coverage | pass | E1 through E4 map to stable tests. |
| Negative and boundary coverage | pass | Closed values, stale state, interruption, rollback, missing ownership, and bypass paths are covered. |
| Proof-level adequacy | pass | Unit, integration, end-to-end, and smoke levels match the owning risks. |
| Milestone mapping | concern | M1 through M4 are distinct, but broad-smoke ownership crosses its required gate. |
| Command validity | block | CMD13's owner cannot perform its first required milestone gate. |
| Fixture and data design | pass | Temporary, local, deterministic fixture families are specified with real archive proof where required. |
| Manual-proof boundary | pass | All claims are deterministically observable; no manual procedure is required. |
| Observability | concern | Diagnostic prose exists but is not tied to stable tests and commands. |
| Determinism and isolation | pass | Raw-byte identities, temporary roots, injected interruption, no network, and no wall-clock dependency are explicit. |
| Scope and non-goals | pass | Runtime certification, external mutation, publication, and Cartesian interaction generation remain excluded. |
| Execution economics | pass | Focused milestone checks precede package and broad-smoke checks. |
| Traceability | block | Acceptance criteria and supplemental normative obligations lack stable mappings. |
| Implementation handoff | block | Implementation would need to infer missing proof assertions and cross-stage command authority. |

## Recommendation

Resolve PBF-TSR1 and PBF-TSR2 in the active test spec, then run test-spec-review R2. No feature-spec, architecture, ADR, or plan revision is required.
