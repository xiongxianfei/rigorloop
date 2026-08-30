# Spec Review R1: Consolidated Review Gates

Review ID: spec-review-r1
Stage: spec-review
Round: r1
Reviewer: Codex independent spec-review context
Target: `specs/consolidated-review-gates.md`
Reviewed artifact: `specs/consolidated-review-gates.md` at `sha256:4a6736414294c454505b1826ae9f7c62775d669226978bc3d0516976ca22456e`
Reviewed artifact path: specs/consolidated-review-gates.md
Reviewed artifact identity: sha256:4a6736414294c454505b1826ae9f7c62775d669226978bc3d0516976ca22456e
Review date: 2026-08-28
Recording status: recorded
Status: changes-requested
Material findings: CRG-SR1, CRG-SR2, CRG-SR3

## Result

- Skill: spec-review
- Review status: changes-requested
- Material findings: CRG-SR1, CRG-SR2, CRG-SR3
- Open blockers: activation classification lacks an authoritative boundary; non-approved package outcomes lack deterministic authority and handoff semantics; proposal-package identity and staleness are internally inconsistent
- Immediate next stage: review-resolution
- Eventual test-spec readiness: not-ready
- Stop condition: downstream planning stops until the findings are dispositioned, the specification is revised, and a current same-stage rereview approves the revised specification

## Recording

- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/reviews/spec-review-r1.md`
- Review log: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-log.md`
- Review resolution: `docs/changes/2026-08-28-consolidate-rigorloop-review-gates/review-resolution.md`

## Governed settlement

- Settlement mode: governed-spec-entry
- Settlement status: blocked until workflow routing enters `spec-review`; review recording remains durable
- Governed change identity: `2026-08-28-consolidate-rigorloop-review-gates`

## Boundary review

- Boundary applicability: `boundary-first-v1` applicable; all eight dimensions are declared, but the compatibility, state, authority, and temporal contracts contain the material gaps below
- Boundary resources: `boundary-first-method-v1.md`, `boundary-first-feature-authoring-v1.md`
- Boundary blocker: CRG-SR1 affects `BND-COMPAT-001` and `BND-STATE-001`; CRG-SR2 affects `BND-STATE-001`, `BND-AUTH-001`, and `BND-RECOVERY-001`; CRG-SR3 affects `BND-INPUT-001` and `BND-TEMPORAL-001`

## Automated review

- Automation mode: manual
- Automation evidence: none
- Automation result: not applicable; semantic review is changes-requested

## Findings

## Finding CRG-SR1

Finding ID: CRG-SR1
Severity: major
Location: glossary `activation`; CRG-R35; CRG-R38; EC10; `BND-COMPAT-001`; Observability
Evidence: CRG-R35 gives opposite meanings to an absent topology marker depending on whether a governed change is pre-activation or post-activation, but the contract defines no authoritative activation identity, durable activation record, comparison input for change creation, or owner of that classification. CRG-R38 lists prerequisites for activation without defining the observable event or state that proves those prerequisites were atomically accepted. A lifecycle reader therefore cannot deterministically choose v1 inheritance versus fail-closed rejection, and compatibility fixtures cannot prove the boundary without inventing architecture-level product behavior.
Required outcome: define the observable activation and change-classification contract, including the authoritative durable input, its owner and identity, how a change is classified relative to it, behavior for missing or ambiguous activation evidence, and the status evidence that exposes the decision. Exact field placement and serialization may remain architecture-owned.
Safe resolution path: require one durable, identity-bound activation record or equivalent authoritative epoch selected by workflow governance; bind each new change to an explicit topology at creation; permit missing-marker v1 inheritance only when the change has provable pre-activation identity; and fail closed when the activation or comparison evidence is absent or ambiguous.
needs-decision rationale: none

## Finding CRG-SR2

Finding ID: CRG-SR2
Severity: major
Location: CRG-R15; CRG-R21; CRG-R29 through CRG-R34; Error and boundary behavior; CRG-AC6
Evidence: the specification closes the outcome vocabulary and defines the authority granted by `approved`, but it does not define deterministic package-state, progression-authority, correction, or immediate-handoff behavior for `changes-requested`, `blocked`, and `inconclusive`. Examples cover only selected `changes-requested` cases. In particular, the contract does not distinguish a reviewable package defect from a missing or contradictory upstream prerequisite or insufficient evidence, nor state whether and how each non-approval outcome settles the attempted package review. Different skills, CLI implementations, and tests could therefore assign different authority and routes to the same outcome.
Required outcome: define a deterministic status-to-authority and handoff mapping for Design Review and Delivery Review covering all four outcomes, including progression permission, package settlement or attempted-review state, allowed correction targets, review-resolution use, missing-input stop behavior, and same-stage rereview requirements.
Safe resolution path: add one normative matrix for both package gates: `approved` grants the gate's stated authority; `changes-requested` grants none and routes artifact-owned defects through review resolution and author revision; `blocked` grants none and names the missing or contradictory upstream owner; `inconclusive` grants none, uses no forward handoff, and records the missing evidence. Require current package rereview whenever correction changes a governed identity.
needs-decision rationale: none

## Finding CRG-SR3

Finding ID: CRG-SR3
Severity: major
Location: glossary `proposal package`, `package manifest`, and `component artifact`; CRG-R10; CRG-R22 through CRG-R24; CRG-R42; EC2
Evidence: CRG-R22 applies exact manifest fields to every package review record and CRG-R42 requires Verify to consume the exact accepted proposal package. Yet only design and delivery packages receive explicit manifest and settlement rules. The proposal package optionally includes cited research, while EC2 makes research staleness depend on a semantic conclusion that the proposal "materially relies" on an exact identity. The specification never says whether cited research is a component artifact, how its applicability enters the manifest, what upstream-package field applies to Proposal Review, or whether its byte changes follow CRG-R24. As written, the universal package identity rule and the conditional proposal-research rule cannot be implemented or tested consistently.
Required outcome: define one coherent proposal-review evidence model. Either include the proposal package in the deterministic manifest, identity, and staleness regime with closed research applicability and field-applicability rules, or explicitly limit the universal package rules to design and delivery and define a distinct exact proposal-review evidence contract that Verify can consume.
Safe resolution path: prefer a proposal-package manifest that always includes the exact proposal revision and includes each explicitly relied-on repository research artifact by normalized path and content identity; define absent upstream identity as inapplicable for Proposal Review; make any included component-byte change stale; and require proposal revision to add or remove relied-on research. If semantic research freshness beyond byte identity is needed, define it as a separate Proposal Review judgment rather than an identity exception.
needs-decision rationale: the specification owner must choose whether Proposal Review participates in the universal package-manifest contract or uses an explicitly separate evidence contract before architecture can select representation.

## Review dimensions

| Review dimension | Verdict | Notes |
| --- | --- | --- |
| requirement clarity | changes requested | Three authority-sensitive behaviors are not deterministic. |
| normative language | pass | Normative terms and closed vocabularies are otherwise used consistently. |
| completeness | changes requested | Activation classification, non-approval mappings, and proposal-package identity are incomplete. |
| testability | changes requested | The missing contracts prevent unique compatibility, routing, and staleness expectations. |
| examples | concern | Examples are strong but do not cover blocked or inconclusive package outcomes or authoritative activation classification. |
| compatibility | changes requested | V1/v2 coexistence cannot be classified deterministically without an activation boundary. |
| observability | concern | Required output is broad, but the authoritative activation input it should report is absent. |
| security/privacy | pass | Paths, private runtime data, authority separation, and local trust boundaries are addressed. |
| non-goals | pass | Representation and command spelling are appropriately deferred; the findings request observable behavior, not architecture. |
| acceptance criteria | changes requested | CRG-AC5 through CRG-AC7 cannot have unique pass/fail results until the findings are resolved. |

## Boundary assessment

The specification classifies all eight boundary dimensions and selects the central design-package, delivery-package, staleness, rollback, hybrid-authority, and generated-parity interactions. Example ownership is explicit. The boundary record is structurally sound, and the absent proof map is the expected downstream `test-spec` dependency rather than an independent defect at this stage. Semantic completeness is not yet established because the compatibility transition lacks an authoritative activation input, the state/authority model lacks non-approval transitions, and the input/temporal model does not coherently include the proposal package.

## Claim limitations

This review records three specification findings only. It does not revise the specification, settle it as approved, route workflow, approve architecture, establish planning or test-spec readiness, validate implementation, or claim branch or PR readiness.
