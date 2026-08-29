# Spec Review R2: Consolidated Review Gates

Review ID: spec-review-r2
Stage: spec-review
Round: r2
Reviewer: Codex independent spec-review context
Target: `specs/consolidated-review-gates.md`
Reviewed artifact: `specs/consolidated-review-gates.md` at `sha256:64fbc97dc179d86b24c9aa04434521f3fe73349b643e9bf7845ed227ebee2a62`
Reviewed artifact path: specs/consolidated-review-gates.md
Reviewed artifact identity: sha256:64fbc97dc179d86b24c9aa04434521f3fe73349b643e9bf7845ed227ebee2a62
Review date: 2026-08-28
Recording status: recorded
Status: changes-requested
Material findings: CRG-SR4

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CRG-SR4
- Open blockers: the aggregate design-package revision does not unambiguously include the accepted Proposal Review binding that can change design staleness
- Immediate next stage: review-resolution
- Eventual test-spec readiness: not-ready
- Stop condition: downstream planning stops until CRG-SR4 is dispositioned, the aggregate upstream-binding rule is revised, and a current same-stage rereview approves the specification

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/spec-review-r2.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: revision-required
- Governed change identity: `2026-08-28-consolidate-rigorloop-review-gates`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable; all eight dimensions remain applicable and structurally complete
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: CRG-SR4 affects `BND-AUTH-001`, `BND-TEMPORAL-001`, and `BND-COMPOSE-001` because an upstream proposal-review change can alter authority without an unambiguous aggregate-revision change

## Automated review

- Automation mode: manual
- Automation evidence: none
- Automation result: not applicable; semantic review is changes-requested

## Findings

## Finding CRG-SR4

Finding ID: CRG-SR4
Severity: major
Location: glossary `package revision`; CRG-R22 through CRG-R24; CRG-R42; `BND-AUTH-001`; `BND-TEMPORAL-001`
Evidence: CRG-R22 correctly says Design Review binds the accepted Proposal Review ID and that no proposal-package revision exists. However, the glossary and CRG-R23 define the aggregate calculation only in terms of an applicable upstream package revision. A Design Review therefore has no defined upstream value for that calculation. If the accepted Proposal Review changes while architecture, specification, and ADR bytes remain unchanged, the text permits the aggregate design-package revision to remain unchanged even though the bound upstream direction changed. That conflicts with CRG-R23's rule that every changed governed input changes the aggregate revision and leaves stale-design behavior implementation-dependent.
Required outcome: define one upstream binding input for aggregate revision calculation and staleness: the accepted Proposal Review ID for a design package and the approved aggregate design-package revision for a delivery package. A changed upstream binding must change the downstream aggregate revision and require current rereview.
Safe resolution path: replace `applicable upstream package revision` with `applicable upstream binding` in the glossary and CRG-R22 through CRG-R26; define its two exact values; include it in aggregate calculation and stale checks; retain accepted proposal evidence outside package settlement and retain one aggregate revision without per-document hashes.
needs-decision rationale: none

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | concern | The upstream aggregate input is inconsistent for Design Review. |
| normative language | pass | Normative terms and closed vocabularies are otherwise precise. |
| completeness | block | One authority-sensitive staleness input lacks a defined value. |
| testability | block | A changed Proposal Review can produce two plausible design-package revision outcomes. |
| examples | pass | Examples remain requirement-owned and cover the central package and compatibility behavior. |
| compatibility | pass | The activation baseline now deterministically classifies markerless legacy changes. |
| observability | concern | Aggregate status is clear once its upstream input is closed. |
| security/privacy | pass | The revision avoids machine-local data and contributor-maintained per-document hashes. |
| non-goals | pass | Command spelling, schema placement, and serialization remain appropriately architecture-owned. |
| acceptance criteria | concern | CRG-AC4 and CRG-AC5 require the missing upstream-binding rule for unique proof. |

## Prior-finding closure assessment

- CRG-SR1 is resolved by the accepted activation baseline, explicit new-change topology assignment, fail-closed non-membership, observable baseline ID, and atomic workflow-governance activation contract.
- CRG-SR2 is resolved by the deterministic four-outcome authority and next-action matrix, separate correction targets, non-approved blocker semantics, and current rereview requirement.
- CRG-SR3 is resolved by keeping accepted proposal evidence outside multi-artifact package settlement and limiting aggregate package records to Design Review and Delivery Review without per-document hashes.

## Boundary assessment

All eight dimensions remain classified and the added outcome and markerless-change interactions close the R1 state, authority, recovery, and compatibility gaps. The only remaining semantic gap is the interaction between accepted Proposal Review authority and aggregate design-package staleness. The missing proof map remains the authorized downstream `test-spec` dependency rather than a separate specification defect.

## Claim limitations

This review does not revise the specification, approve architecture, establish planning or test-spec readiness, validate implementation, or claim branch or PR readiness.
