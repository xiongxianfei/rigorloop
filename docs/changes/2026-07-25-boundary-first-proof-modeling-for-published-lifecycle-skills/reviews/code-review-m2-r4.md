# Code Review M2 R4

Review ID: code-review-m2-r4

Stage: code-review

Round: 4

Reviewer: Codex code-review skill

Target: commit range e522a808..6a3259bf

Reviewed artifact: corrected M2 implementation and immutable run
`run-95e4759a48cb46d183b8222e73ecc5ec`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-10

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-implementation-r3

Reviewer context ID: boundary-m2-review-r4-reset

Context separation mechanism: fresh review phase with tracked-diff reset

Risk tier: elevated

Risk-tier triggers: durable publication transaction; interruption recovery;
immutable evidence authority; high-risk M2

Risk-tier classifier: governing-spec and changed-path triggers

Governing artifacts: specs/rigorloop-workflow.md R28y;
specs/rigorloop-workflow.test.md T51-T52;
docs/architecture/system/architecture.md;
docs/plans/2026-07-25-boundary-first-proof-modeling.md M2

Formal criteria: R28y; R28n; T51; T52; BFP-CR-M2-8

Initial packet inventory: specs/rigorloop-workflow.md@6a3259bf#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@6a3259bf#sha256:83258b4574436d799ac33021fc770dbc37b2b21fc85c60e20664cd901732d067; docs/architecture/system/architecture.md@6a3259bf#sha256:ee9cda306ac94b7f23be63f59353ae453c7792e8f7a5bda9af8ca603f007ac1d; docs/plans/2026-07-25-boundary-first-proof-modeling.md@6a3259bf#sha256:b346a8e2922a18d596b187d7186a388e0545c12e70530512ea90e583d9d6aa65; scripts/boundary_proof_behavior.py@6a3259bf#sha256:5c51cbe1aaf1caa1bfdcc7c23654399df267ed9067cfb829fe1b9319ab767d27; scripts/test-boundary-proof.py@6a3259bf#sha256:94f7d332a03e7f64a52294c7feb06d4aae3da6ef0a8696e1c662e787363a6924

Prompt template version: code-review-template-v1

Initial packet hash: sha256:2070fbb1305f4906a8e06816945356ae88e0a91b2b26df5f766e7a73c4558544

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: M2 stage invocation, immutable-run construction,
publication, interruption recovery, current-pointer authority, and validation

Highest-impact failure modes: two publishers can share no durable ownership
record; an interruption before `prepared.json` is indistinguishable from an
orphan; a run manifest cannot be bound to the publisher that created it;
recovery may discard or repeat work outside the approved state machine

Changed boundaries: global recovery discovery, publisher ownership,
working/staging/target roots, prepared receipt, immutable manifest, current
pointer

Evidence expected: exact publisher lease and manifest schemas; lease-first
publication; global-state recovery matrix; crash-boundary regressions;
canonical run bound to publisher instance

Areas requiring direct inspection: R28y publisher and recovery contract;
`_assemble_run`; `_publish_run`; `_reconcile_prepared`; immutable current
manifest; T51-T52 proof map

Areas intentionally out of scope: M3 downstream preservation; M4 aggregation;
final explain-change, verify, PR, hosted CI, and release activation

Risk classes considered: durable-write ordering=applicable;
interruption recovery=applicable; concurrency/idempotency=applicable;
identity freshness=applicable; generated-evidence currency=applicable;
security/privacy=not-applicable:no secret or credential surface changed

Falsifiable review questions: Does a durable lease exist before the first
stage invocation? Does every run bind the publisher instance? Can every
lease-only, working, staging, prepared, installed, pointer, and cleanup
interruption state resume without reinvocation or unsafe deletion? Does the
test spec directly prove those states?

Clean-review sufficiency receipt: no

Requirement-fidelity gate: required

Requirement-fidelity applicability: applicable

Requirement-fidelity affected paths: scripts/boundary_proof_behavior.py; scripts/test-boundary-proof.py; specs/rigorloop-workflow.test.md

Requirement-fidelity matched path triggers: specs/

Requirement-fidelity matched category triggers: workflow routing contracts

Requirement-fidelity review stage: code-review

Requirement-fidelity packet order: spec clause > decomposition > expected
surfaces > implementation diff > validator assertions > validation evidence >
prior findings

Requirement-property decomposition evidence: present below

Requirement-fidelity receipt: no; material compression found

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: this review record, review log, review resolution, active
  plan, and plan index
- Open blockers: BFP-CR-M2-10
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-10
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r4.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-10
- Verify readiness: not-claimed

## Review inputs

- Diff: `e522a808..6a3259bf`
- Tracked governing branch state: clean at
  `6a3259bf29604b126439f1aaa9871f964324b8fe`
- Governing contract: R28y and R28n
- Proof map: T51 and T52
- Active plan: M2
- Validation evidence: current immutable behavior result plus focused,
  skill, build, lifecycle, metadata, and review-artifact validators

## Diff summary

The reviewed slice adds capability-bound upstream stage execution, a closed
transport coordinator, stage-authored envelope materialization, parent-only
candidate comparison, bounded correction assembly, immutable run evidence,
published boundary guidance, and the current M2 handoff.

It also revises R28y's recovery contract. The implementation does not project
that complete contract.

## Requirement-property decomposition

| R28y property | Required surfaces | Observed implementation | Result |
| --- | --- | --- | --- |
| Lease precedes lifecycle invocation | publisher state; generation flow; recovery tests | no `publisher.json` writer or lease validator exists | fail |
| Run binds publisher identity | exact manifest schema; staged/install validation | current manifest omits `publisher_instance_id` | fail |
| Global recovery selects one candidate | discovery evaluator; conflict tests | only `prepared.json` reconciliation is implemented | fail |
| Working, staging, and target roots are lease-bound | publication flow; crash tests | publication starts from an unleased temporary directory | fail |
| Proof map covers every `MUST` | T51-T52 and direct regressions | test spec contains no publisher-instance or publisher-lease obligation | fail |

## Finding

### BFP-CR-M2-10 - Publisher lease and global recovery contract are absent

Finding ID: BFP-CR-M2-10

Prior finding reconciliation: failed-remediation

Severity: blocker

Auto-fix class: declared-safe

Location:

- `specs/rigorloop-workflow.md`, R28y publisher and recovery transaction
- `specs/rigorloop-workflow.test.md`, T51-T52
- `scripts/boundary_proof_behavior.py`, run assembly, publication, and recovery
- current immutable run manifest

Evidence:

- R28y requires `publisher.json` to be exclusively written and fsynced before
  lifecycle invocation.
- R28y requires every run manifest to contain `publisher_instance_id`.
- The current immutable manifest contains only `run_id`, `input_set`,
  `input_set_identity`, `baseline_commit`, inventories, snapshots, transport
  attempts, and events.
- `scripts/boundary_proof_behavior.py` contains no publisher lease schema,
  writer, validator, or global recovery selector.
- T51-T52 contain no `publisher_instance_id` or publisher-lease proof.

Required outcome: Implement and directly prove the complete approved
lease-first publication and global recovery contract before treating M2
evidence as current.

Safe resolution path:

- Inputs: exact R28y lease, run-manifest, prepared-receipt, pointer, global
  discovery, and recovery-state contracts.
- Outputs: closed typed lease/state validators; lease-first working-root
  creation; publisher-bound manifest and receipt; global candidate selection;
  evidence-first resume/cleanup; regenerated current run.
- Allowed paths: R28y proof-map text, M2 harness/model/tests, current M2
  evidence, review resolution, and active-plan state.
- Forbidden paths: M3/M4 skill behavior, release activation, external actions,
  PR/deployment surfaces, and unrelated refactors.
- Acceptance criteria: every exact schema and closed global state has direct
  positive/negative proof; unknown or conflicting state fails closed; every
  crash boundary resumes without lifecycle reinvocation; current run includes
  a valid publisher identity; all M2 validation and lifecycle state-sync
  checks pass.
- Required validation: T51-T52 focused tests, complete boundary-proof suite,
  canonical generate/validate, skill/build validators, review/metadata/
  lifecycle validators, and diff integrity.

No owner decision is required because the approved spec already selects the
transaction and recovery semantics.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Lease-first and publisher-bound R28y properties are absent. |
| Test coverage | block | T51-T52 compress the publisher/recovery contract and cannot catch the omission. |
| Edge cases | block | Lease-only, working-root, staging-root, and global conflict states lack direct proof. |
| Error handling | concern | Existing prepared-receipt recovery is fail-closed but covers only a subset of the approved state machine. |
| Architecture boundaries | block | Durable publication ownership is missing from the implementation boundary. |
| Compatibility | pass | Opaque v1 and unsupported v2 behavior are unaffected by this finding. |
| Security/privacy | pass | No secret or private-data exposure was found. |
| Derived artifact currency | block | The current run is structurally valid under code but not under the exact R28y manifest schema. |
| Unrelated changes | pass | The reviewed changes remain within the boundary-first initiative. |
| Validation evidence | concern | The commands pass, but the proof map omits the failing publisher properties. |

## Prior finding reconciliation

- `BFP-CR-M2-1`: resolved.
- `BFP-CR-M2-7`: resolved.
- `BFP-CR-M2-8`: prior remediation was incomplete.
- `BFP-CR-M2-10`: new failed-remediation finding records the omitted
  publisher-lease and global-recovery properties without reusing an existing
  finding identity.
- `BFP-CR-M2-9`: resolved.

## Handoff

M2 returns to `resolution-needed`.
Revise and review the T51-T52 proof map before implementing the publisher
lease and global recovery contract.
M3, final closeout, verify, and PR handoff remain blocked.
