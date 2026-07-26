# Boundary-First Proof Modeling Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: M1 R1
Reviewer: Codex code-review skill with context-separated blind-first reviewer
Target: commit `a6300a9a` against `8da98fe1`
Reviewed artifact: M1 implementation commit `a6300a9a`
Reviewed milestone: M1. Typed model, validator, fixtures, and report core
Status: changes-requested
Review status: changes-requested
Review date: 2026-07-26
Recording status: recorded
Material findings: BFP-M1-CR1, BFP-M1-CR2, BFP-M1-CR3, BFP-M1-CR4, BFP-M1-CR5, BFP-M1-CR6, BFP-M1-CR7
Immediate next stage: owner decision for BFP-M1-CR4, BFP-M1-CR6, and BFP-M1-CR7
Automated review: yes
Native review status: changes-requested
Review gate outcome: stop
Independence level: L2
Author context ID: boundary-first-m1-author
Reviewer context ID: boundary-first-m1-blind-reviewer
Context separation mechanism: separate-agent
Author context excluded: true
Risk tier: elevated
Risk-tier triggers: new fail-closed contract projection, capability-report evidence claims, fixture replay boundary
Risk-tier classifier: changed-contract-and-evidence-surface
Governing artifacts: specs/rigorloop-workflow.md; specs/skill-contract.md; specs/rigorloop-workflow.test.md; specs/skill-contract.test.md; docs/architecture/system/architecture.md; docs/adr/ADR-20260725-boundary-first-proof-modeling.md; docs/plans/2026-07-25-boundary-first-proof-modeling.md
Formal criteria: R28-R28e, R28k, R28p-R28y, R56m, R56o-R56p, T40-T49, T51, T55
Initial packet inventory: specs/rigorloop-workflow.md@a6300a9a#sha256:bed5b028aa08cefbf5d497cb81ba3245993466778e0fcabf522e2ff37a58c634; specs/skill-contract.md@a6300a9a#sha256:d19b30d1890b5e7834b976192465694077cef7bcee01152f9744741b02b0a566; specs/rigorloop-workflow.test.md@a6300a9a#sha256:074cd1e8df71b9972d2908d6d413b6143bfe11a5a3826caaacb4e851b65bb763; specs/skill-contract.test.md@a6300a9a#sha256:416b1718102c80cdfceb146b0d2f171b2d3f4259d034ec10d84c4e838fa0f767; docs/plans/2026-07-25-boundary-first-proof-modeling.md@a6300a9a#sha256:0f7eeb6a1789578eb16c7b70ec37f9bd7a3bb4d196e35f7930daf12c19789941
Prompt template version: review-gate/v1
Initial packet hash: sha256:49bd12304a0e5580fc2ecd37c503aff9fd2c5df2b96ccb821b0653a96a56bf01
Manifest owner: workflow orchestrator
Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded
Clean-review sufficiency receipt: no

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, `review-log.md`, `review-resolution.md`, the active plan, plan index, and `change.yaml`
- Open blockers: three findings require owner decisions because the approved implementation contract does not define the missing representation or harness boundary
- Next stage: owner decision, then review-resolution M1
- Review status: changes-requested
- Material findings: BFP-M1-CR1 through BFP-M1-CR7
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md`
- Review resolution: `docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md#code-review-m1-r1`
- Reviewed milestone: M1. Typed model, validator, fixtures, and report core
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1 resolution needed, M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-M1-CR1 through BFP-M1-CR7
- Verify readiness: not-claimed

## Independent Risk Map

Affected behavior: the closed typed boundary model, proof-map traceability, legacy/v1 parity, incident registry, capability aggregation, deterministic report serialization, and the compact simple-change proof.

Highest-impact failure modes: false traceability; partial legacy state; detached evidence; noncanonical report bytes; registry labels mistaken for executable incident proof; asserted rather than derived workflow-overhead results.

Changed boundaries: approved specs to typed projection; untrusted records to normalized models; boundary ownership to proof obligations; validated aggregate to report bytes; fixture registry to gate evidence.

Evidence expected: exact clause-to-field projection, contrast tests for every closed value, requirement-to-boundary pairing, full parity matrix, repository-visible evidence, canonical serialization, executable incident replay, and derived simple-change workflow observations.

Areas requiring direct inspection: the three M1 scripts, both boundary-proof fixtures, exact commit path inventory, and M1 governing clauses.

Areas intentionally out of scope: M2-M4 public skill behavior, adapters, activation, publication, external systems, and semantic taxonomy judgment.

Risk classes considered: contract projection, fail-closed ordering, requirement compression, compatibility, evidence claims, deterministic serialization, fixture escape, and scope containment. Network behavior, credentials, external actions, release rollback, throughput, and public adapter execution are non-applicable.

Falsifiable review questions: can unrelated known requirements satisfy traceability; can malformed example IDs pass; can partial legacy state pass; can nonexistent evidence pass; can mapping order change report bytes; are incident and simple-change claims computed by an executable harness?

## Evidence Challenge and Direct Proof

The reviewer inspected the commit before receiving author validation summaries.
After `risk-map-recorded`, the orchestrator released the focused test and
lifecycle evidence. The reviewer reproduced the 12 passing M1 tests, then ran
direct adversarial probes that demonstrated acceptance of:

- a changed seeded-omission description;
- a proof boundary paired with an unrelated globally known requirement;
- invalid and duplicate regression IDs;
- partial and mismatched legacy scope state;
- nonexistent report evidence;
- `not-run` evidence without a blocking reason; and
- different report bytes for semantically equivalent reordered mappings.

The ten changed commit paths are all M1 implementation, fixture, plan, or
change-local evidence surfaces. No unrelated skill, adapter, selector, or
release behavior changed.

## Findings

### BFP-M1-CR1: False traceability and invalid regression identities are accepted

Finding ID: BFP-M1-CR1
- Severity: blocker
- Status: open
- Location: `scripts/boundary_proof_model.py:450`, `scripts/boundary_proof_model.py:573`, `scripts/boundary_proof_model.py:596`
- Evidence: Regression and discovery IDs receive only non-empty-string checks and no artifact-class uniqueness check. Proof requirements are compared with a global requirement set rather than the requirements governing each referenced boundary or interaction. Direct invalid-ID, duplicate-ID, and unrelated-known-requirement probes passed.
- Required outcome: Enforce stable and unique regression/discovery IDs and bind every proof row's requirements to its referenced boundaries and interactions.
- Safe resolution path: Build owner-requirement sets per boundary and interaction, require each reference to share a cited governing requirement, reject citations governing none of the references, and add direct negative regressions.
- auto_fix_class: declared-safe
- deterministic_recipe: derive reference ownership from normalized feature rows; add stable-ID and per-class uniqueness checks; add invalid, duplicate, unrelated-known, and mixed-reference tests
- named_inputs: approved R28s, R28u, R28w and normalized feature records
- named_outputs: stricter model normalization and direct regression tests
- allowed_paths: `scripts/boundary_proof_model.py`; `scripts/test-boundary-proof.py`
- forbidden_paths: specs; plans; skills; adapters; lifecycle evidence
- acceptance_criteria: all three reproduced escapes fail with stable diagnostics and existing valid fixtures pass
- required_validation: `python scripts/test-boundary-proof.py`; targeted probes; M1 script compilation
- needs-decision rationale: none

### BFP-M1-CR2: The frozen incident registry does not freeze omission classes

Finding ID: BFP-M1-CR2
- Severity: blocker
- Status: open
- Location: `scripts/boundary_proof_model.py:650`, `scripts/boundary_proof_model.py:672`, `scripts/test-boundary-proof.py:402`
- Evidence: `FIXTURE_GATES` freezes only ID-to-gate mappings. Any non-empty `seeded_omission` passes, and tests mutate only the fixture ID.
- Required outcome: Freeze exact fixture ID, seeded-omission class, and owning gate for all eight R28x rows.
- Safe resolution path: Replace the gate-only map with one immutable exact registry and add independent omission and gate mutation tests.
- auto_fix_class: mechanical
- auto_fix_kind: closed-vocabulary-entry
- affected_paths: `scripts/boundary_proof_model.py`; `scripts/test-boundary-proof.py`; `tests/fixtures/boundary-proof/incident-registry.json`
- deterministic_authority: R28x exact eight-row incident registry
- required_validation: `python scripts/test-boundary-proof.py`; targeted registry mutation probes
- needs-decision rationale: none

### BFP-M1-CR3: Legacy/version parity accepts partial marker state

Finding ID: BFP-M1-CR3
- Severity: blocker
- Status: open
- Location: `scripts/boundary_proof_model.py:773`
- Evidence: Scope parity is enforced only for `v1`; missing markers normalize independently to `legacy`. Stray scope on a markerless artifact and explicit legacy markers with mismatched scopes passed.
- Required outcome: Keep marker presence, version, scope presence, and scope value synchronized; grandfather only the completely markerless legacy pair.
- Safe resolution path: Enforce symmetric marker presence, forbid scope on markerless legacy pairs, require matching valid scopes for explicit `legacy` and `v1`, and preserve reviewed opt-in for pre-activation `v1`.
- auto_fix_class: declared-safe
- deterministic_recipe: implement R28r's closed marker/scope matrix and table-driven contrast tests
- named_inputs: feature/test version markers, scopes, activation state, reviewed opt-in
- named_outputs: exhaustive parity decision and regressions
- allowed_paths: `scripts/boundary_proof_model.py`; `scripts/test-boundary-proof.py`
- forbidden_paths: specs; skills; adapters; unrelated artifact parsers
- acceptance_criteria: partial/mismatched legacy cases fail; fully markerless legacy and matching reviewed v1 pass
- required_validation: `python scripts/test-boundary-proof.py`; full parity matrix probe
- needs-decision rationale: none

### BFP-M1-CR4: Capability-report evidence can be nonexistent or semantically invalid

Finding ID: BFP-M1-CR4
- Severity: blocker
- Status: open
- Location: `scripts/boundary_proof_model.py:678`, `scripts/boundary_proof_model.py:750`, `scripts/test-boundary-proof.py:436`
- Evidence: `evidence_refs` proves only non-empty strings. A nonexistent path passes, and `not-run` can cite a normal path rather than a blocking reason.
- Required outcome: Define and enforce repository-visible current evidence for pass/fail rows and a closed blocking-reason representation for `not-run`.
- Safe resolution path: Select a repository-root-aware evidence identity contract, reject unsafe/missing/non-regular/out-of-root evidence, and add missing, stale/substituted, unsafe, and wrong-kind contrasts.
- auto_fix_class: none
- needs-decision rationale: The approved implementation contract does not define the evidence identity/freshness representation, so implementation must not invent path-fragment or hash semantics.

### BFP-M1-CR5: Capability-report serialization is not deterministic

Finding ID: BFP-M1-CR5
- Severity: major
- Status: open
- Location: `scripts/validate-boundary-proof.py:29`, `scripts/validate-boundary-proof.py:33`
- Evidence: `_render_report` uses `sort_keys=False`; accepted report mappings may arrive in arbitrary order. Reordering only the checks mapping changed output bytes.
- Required outcome: Semantically equivalent validated report data must serialize to one canonical byte representation.
- Safe resolution path: Render a canonical field-order projection or sorted mappings while preserving contractually ordered lists, and add permutation byte-equality tests.
- auto_fix_class: mechanical
- auto_fix_kind: deterministic-serialization
- affected_paths: `scripts/validate-boundary-proof.py`; `scripts/test-boundary-proof.py`
- deterministic_authority: R28y deterministic report and architecture sole-writer boundary
- required_validation: `python scripts/test-boundary-proof.py`; report permutation probe
- needs-decision rationale: none

### BFP-M1-CR6: The incident corpus is not replayable

Finding ID: BFP-M1-CR6
- Severity: blocker
- Status: open
- Location: `tests/fixtures/boundary-proof/incident-registry.json`, `scripts/test-boundary-proof.py:402`
- Evidence: The repository contains only incident descriptors. No seeded omission passes through an owning gate, and no test proves detected stage, code-review escape, or sibling bypass.
- Required outcome: Provide one executable seeded omission per R28x ID and demonstrate detection no later than its owning gate.
- Safe resolution path: Select a reviewed fixture payload and owning-gate harness with detected-stage, escape, and sibling-bypass assertions.
- auto_fix_class: none
- needs-decision rationale: The approved implementation contract does not assign the fixture payload representation or gate-harness ownership.

### BFP-M1-CR7: The simple-change fixture asserts rather than derives workflow evidence

Finding ID: BFP-M1-CR7
- Severity: blocker
- Status: open
- Location: `tests/fixtures/boundary-proof/simple-change.json`, `scripts/test-boundary-proof.py:442`
- Evidence: The test normalizes static structures and directly asserts supplied counters. It executes no workflow stage, false-blocking observation, correction loop, or artifact-count derivation.
- Required outcome: Exercise the same workflow and derive applicable-only mappings, universal-artifact count, false blocking, and correction-cycle evidence.
- Safe resolution path: Select a simple-change trace/harness whose observations compute these values and prove at most one structural correction with zero false blocking.
- auto_fix_class: none
- needs-decision rationale: The approved implementation contract does not define the workflow trace or harness ownership, so implementation cannot safely choose it.

## Requirement Fidelity

| Contract surface | Result | Evidence |
| --- | --- | --- |
| Closed typed projection | concern | Core IDs and immutable records exist, but example identity fidelity is incomplete. |
| Applicability and extension rules | pass | Exact fields, conditional applicability, namespaced extensions, and `other` rejection are enforced. |
| Example and interaction semantics | block | BFP-M1-CR1 leaves stable and unique regression/discovery identity incomplete. |
| Proof traceability | block | BFP-M1-CR1 permits unrelated globally known requirements. |
| Prospective version parity | block | BFP-M1-CR3 permits partial and contradictory legacy state. |
| Incident registry and replay | block | BFP-M1-CR2 and BFP-M1-CR6 leave exact classes and executable replay incomplete. |
| Capability aggregation/report | block | BFP-M1-CR4 and BFP-M1-CR5 leave evidence validity and canonical bytes incomplete. |
| Simple-change overhead proof | block | BFP-M1-CR7 accepts asserted rather than derived evidence. |
| Semantic-authority boundary | pass | The typed model explicitly declines semantic completeness judgments. |
| Scope containment | pass | All ten paths are M1 implementation, fixture, plan, or change-local evidence. |

## Prior Finding Reconciliation

No prior M1 findings existed. `prior-findings-released` records an empty prior
finding set after the blind-first risk map and evidence challenge.

## Milestone Handoff

- Reviewed milestone: M1. Typed model, validator, fixtures, and report core
- Review status: changes-requested
- Milestone state after review: resolution-needed
- Required review-resolution: yes
- Remaining in-scope implementation milestones: M1 resolution needed, M2, M3, M4
- Next stage: owner decision for BFP-M1-CR4, BFP-M1-CR6, and BFP-M1-CR7
- Final closeout readiness: not ready because seven M1 findings remain open and three require contract decisions.

## Recommended Next Stage

Keep the automated run paused. Resolve the evidence-identity, executable
incident-harness, and simple-change trace ownership decisions before deriving
implementation-correction authority. Then apply all seven findings as one
bounded M1 correction, rerun focused validation, and independently rereview M1.
