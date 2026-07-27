# Code Review M2 R5

Review ID: code-review-m2-r5

Stage: code-review

Round: 5

Reviewer: Codex code-review skill

Target: commit range 8dce1866..dc7fc15f

Reviewed artifact: lease-first M2 correction and immutable run
`run-c9cf75951ba54219a13fe8f7c237c63d`

Reviewed milestone: M2

Status: changes-requested

Review status: changes-requested

Material findings: BFP-CR-M2-11

Immediate next stage: review-resolution

Milestone closeout: resolution-needed

Recording status: recorded

Review date: 2026-07-27

Automated review: yes

Native review status: changes-requested

Review gate outcome: stop

Independence level: L1

Author context ID: boundary-m2-recovery-implementation-r5

Reviewer context ID: boundary-m2-review-r5-reset

Context separation mechanism: fresh review phase with tracked-diff reset

Risk tier: elevated

Risk-tier triggers: durable publication transaction; interruption recovery;
immutable evidence authority; high-risk M2

Risk-tier classifier: governing-spec and changed-path triggers

Governing artifacts: specs/rigorloop-workflow.md R28y;
specs/rigorloop-workflow.test.md T51-T52;
docs/architecture/system/architecture.md;
docs/plans/2026-07-25-boundary-first-proof-modeling.md M2

Formal criteria: R28y; R28n; T51; T52; BFP-CR-M2-10

Initial packet inventory: specs/rigorloop-workflow.md@dc7fc15f#sha256:7d32316ec3434641ef1fc6512a03deef765a4e264a507300ddf1ab3b4215ee1d; specs/rigorloop-workflow.test.md@dc7fc15f#sha256:8c660c1728b189c87646f089bff3ee12c16f793c8691d26143cf2086378e23b1; docs/architecture/system/architecture.md@dc7fc15f#sha256:ee9cda306ac94b7f23be63f59353ae453c7792e8f7a5bda9af8ca603f007ac1d; docs/plans/2026-07-25-boundary-first-proof-modeling.md@dc7fc15f#sha256:38c5c5a345846a1f024fb6ea861ad9aa8a67c80a96ca6572b3c9dca2f82fe890; scripts/boundary_proof_behavior.py@dc7fc15f#sha256:8bb9028467a329924ae2b63d0c70e50cc35a076a436da23d60c61aa06bbf5f08; scripts/test-boundary-proof.py@dc7fc15f#sha256:cddd271ca63063f7e7c4a14331ce12eefacc6428d586f42a1e93a831e74f5d02

Prompt template version: code-review-template-v1

Initial packet hash: sha256:9b09d5931d4a6f0fc4e832803d500c73474a3392094e10c169c60edec522bcfe

Manifest owner: orchestrator

Phase receipts: risk-map-recorded > evidence-menu-released > evidence-results-released > prior-findings-released > verdict-recorded

Affected behavior: global publisher-state discovery, completed recovery
classification, orphan validation, recovery intent installation, quarantine,
and later fresh generation

Highest-impact failure modes: malformed history is trusted as terminal;
unapproved working bytes are detached under durable authority; invalid staged
bytes bypass staged-run validation; malformed recovery intent cannot use the
approved constrained cleanup path

Changed boundaries: global transient grammar; completed versus active recovery;
minimum-valid working roots; staged-orphan validity; temporary-basis recovery

Evidence expected: exact nested recovery validators; closed candidate and
recovery state evaluators; approved-path working-root validation; complete
staged-run validation; direct negative and crash-resume proof for every T51
property

Areas requiring direct inspection: R28y global discovery and manual recovery;
`_discover_global_candidate`; `discard_interrupted_publication`;
`_tree_identity`; T51 property tests

Areas intentionally out of scope: M3 downstream preservation; M4 aggregation;
final explain-change, verify, PR, hosted CI, and release activation

Risk classes considered: durable-write ordering=applicable;
interruption recovery=applicable; concurrency/idempotency=applicable;
identity freshness=applicable; generated-evidence currency=applicable;
security/privacy=not-applicable:no secret or credential surface changed

Falsifiable review questions: Can malformed completed history disappear from
the active projection? Can recovery detach a working tree containing an
unapproved path? Can recovery accept staging that is not a valid complete run?
Can a well-named malformed temporary basis reach constrained cleanup and
authority-bound reconstruction?

Clean-review sufficiency receipt: no

Requirement-fidelity gate: required

Requirement-fidelity applicability: applicable

Requirement-fidelity affected paths: scripts/boundary_proof_behavior.py;
scripts/test-boundary-proof.py; specs/rigorloop-workflow.test.md

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
  plan, change metadata, and plan index
- Open blockers: BFP-CR-M2-11
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: BFP-CR-M2-11
- Recording status: recorded
- Recording blocker: none
- Review record: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/reviews/code-review-m2-r5.md
- Review log: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-log.md
- Review resolution: docs/changes/2026-07-25-boundary-first-proof-modeling-for-published-lifecycle-skills/review-resolution.md
- Reviewed milestone: M2
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M2, M3, M4
- Required review-resolution: yes
- Finding IDs: BFP-CR-M2-11
- Verify readiness: not-claimed

## Review inputs

- Diff: `8dce1866..dc7fc15f`
- Tracked governing branch state: clean at
  `dc7fc15f5881089f160b10651334285c5e8d4cd0`
- Governing contract: R28y and R28n
- Proof map: T51 and T52
- Active plan: M2
- Direct review probes: malformed completed history, unknown working
  descendant, invalid staged orphan, and malformed temporary basis

## Diff summary

The correction adds a durable publisher lease, publisher-bound manifests and
receipts, global transient discovery, evidence-bound manual recovery,
crash-resumable recovery state, hermetic child workspaces, and a fresh
publisher-bound immutable run.

Those improvements close the normal publication path, but the recovery
implementation still models selected examples rather than the complete closed
R28y state and validation boundaries.

## Requirement-property decomposition

| R28y property | Required surfaces | Direct observation | Result |
| --- | --- | --- | --- |
| Completed history is valid only under every basis/state/quarantine invariant | exact nested validators; global discovery; negative matrix | a three-field malformed basis plus invalid recovery ID is removed from the active projection | fail |
| Working recovery accepts only the minimum-valid approved workspace tree | working-root validator; recovery route; unknown/symlink/special/path tests | an unknown top-level file is accepted, quarantined, and completed | fail |
| Staging recovery requires a complete lease-bound staged run | staged-run validator; recovery route; malformed/incomplete/stale tests | a staging directory containing only `junk` is accepted and completed | fail |
| One well-named malformed temp has constrained locked cleanup | global classifier; recovery cleanup; crash-resume tests | malformed JSON stops with generic identity failure and cannot reconstruct authorized recovery | fail |
| Every T51 property proves its complete negative boundary | separately named direct tests | eight names exist, but the tests exercise representative examples and miss the four executable escapes above | fail |

## Finding

### BFP-CR-M2-11 - Recovery remains example-implemented instead of boundary-complete

Finding ID: BFP-CR-M2-11

Prior finding reconciliation: failed-remediation

Severity: blocker

Auto-fix class: declared-safe

Location:

- `scripts/boundary_proof_behavior.py`, `_discover_global_candidate`
- `scripts/boundary_proof_behavior.py`, `discard_interrupted_publication`
- `scripts/boundary_proof_behavior.py`, `_tree_identity`
- `scripts/test-boundary-proof.py`, T51 publisher and recovery tests

Evidence:

- A malformed minimal basis/state pair with `state: completed` makes
  `_discover_global_candidate` return no active candidate.
- Recovery completes after the working root gains
  `unknown-outside-approved-workspace`.
- Recovery completes after the working root is renamed to staging and contains
  only a `junk` file.
- A single well-named truncated temporary basis fails before the approved
  constrained cleanup/reconstruction route.
- The T51 test names exist, but their assertions do not exercise these required
  negative boundaries.

Required outcome: Project the complete R28y global-discovery and manual-recovery
contract into closed validators and state evaluators, then prove every T51
property with direct positive, negative, conflict, and crash-resume cases.

Safe resolution path:

- Inputs: exact R28y path grammar, basis/state/nested schemas, completed-history
  predicate, minimum-valid working paths, staged-run contract, and malformed
  temporary-basis exception.
- Outputs: typed validation results used by both discovery and recovery;
  closed active/completed classification; constrained cleanup; exhaustive T51
  regression matrix; regenerated canonical evidence only if current input
  identities change.
- Allowed paths: M2 harness/tests/evidence, validation notes, review resolution,
  and active-plan state.
- Forbidden paths: M3/M4 skill behavior, release activation, external actions,
  PR/deployment surfaces, and unrelated refactors.
- Acceptance criteria: all four direct probes fail closed or take the exact
  approved recovery route; every nested field and state tuple has direct
  mutation proof; no recovery adopts bytes or invokes lifecycle skills;
  focused, canonical, skill/build, metadata, review, and lifecycle validation
  pass.
- Required validation: complete boundary-proof suite; four direct adversarial
  regressions; canonical validate and regenerate if input identities change;
  skill/build validators; review/metadata/lifecycle validators; diff
  integrity.

No owner decision is required because the accepted R28y contract already
selects the behavior.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Four mandatory R28y recovery boundaries have executable escapes. |
| Test coverage | block | Named T51 rows exist but do not prove their complete negative obligations. |
| Edge cases | block | Malformed history, unknown working content, invalid staging, and malformed temp handling are missing. |
| Error handling | block | Invalid orphan bytes can be durably detached as authorized recovery. |
| Architecture boundaries | concern | Publisher ownership is present, but the recovery evaluator is not a closed typed projection. |
| Compatibility | pass | Opaque v1 and unsupported v2 behavior are outside the failing paths. |
| Security/privacy | pass | No secret or private-data exposure was found. |
| Derived artifact currency | concern | The current run passes, but does not prove the defective recovery branches. |
| Unrelated changes | pass | The reviewed changes remain within M2. |
| Validation evidence | block | Passing suites omit direct cases that reproduce the defects. |

## Prior finding reconciliation

- `BFP-CR-M2-10`: failed-remediation; the lease and normal publisher path are
  implemented, but global recovery remains materially incomplete.
- `BFP-CR-M2-11`: new residual finding for the independently reproduced
  recovery-boundary escapes.

## Handoff

M2 remains `resolution-needed`.
Enter review resolution for `BFP-CR-M2-11`, add failing direct regressions,
implement the closed recovery projection, and rerun code review.
M3, final closeout, verify, and PR handoff remain blocked.
