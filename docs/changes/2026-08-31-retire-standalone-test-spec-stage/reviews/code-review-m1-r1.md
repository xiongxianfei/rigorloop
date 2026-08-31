# Code Review M1 R1

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Codex code-review skill
Target: M1. Establish frozen contract classification and compatibility
Reviewed artifact: commit `0bf2a805` (`M1: add lifecycle contract classification`)
Review date: 2026-08-31
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/code-review-m1-r1.md`, `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md`, and `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md`
- Open blockers: `RTS-M1-CR1`, `RTS-M1-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `RTS-M1-CR1`, `RTS-M1-CR2`
- Recording status: recorded
- Recording blocker: none; the durable review surfaces record the non-clean result while milestone lifecycle state remains unchanged pending resolution
- Review record: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-log.md`
- Review resolution: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/review-resolution.md`
- Reviewed milestone: M1. Establish frozen contract classification and compatibility
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `RTS-M1-CR1`, `RTS-M1-CR2`
- Verify readiness: not-claimed

## Scope

Reviewed the M1 implementation against the actual commit diff, the approved Design and Delivery packages, the M1 allocation, the matching legacy-path test specification, the implementation evidence, and direct boundary probes. This is an isolated review invocation: it records findings but does not alter implementation or advance lifecycle routing.

## Review inputs

- Diff/review surface: commit `0bf2a805`
- Tracked governing branch state: commit `0bf2a805` on `proposal/retire-standalone-test-spec-stage`
- Approved Design package: `design-review-r2`
- Approved Delivery package: `delivery-review-r3`
- Primary architecture: `docs/architecture/2026-08-31-retire-standalone-test-spec-stage.md`
- Specification: `specs/retire-standalone-test-spec-stage.md`
- Plan: `docs/plans/2026-08-31-retire-standalone-test-spec-stage.md`, approved identity `sha256:727b5a71f1d5ce001876cde59f195536c9671b4743e50a70ef95cf437ccc9938`
- Legacy-path test specification: `specs/retire-standalone-test-spec-stage.test.md`
- Implementation evidence: `docs/changes/2026-08-31-retire-standalone-test-spec-stage/evidence/m1-contract-classification.md`
- Relevant requirements and acceptance criteria: `RTS-R18`, `RTS-R20` through `RTS-R23`, `RTS-AC7`, `RTS-AC8`, `RTS-AC10`
- Relevant boundaries and integrations: `BND-STATE-001`, `BND-TEMPORAL-001`, `BND-RECOVERY-001`, `BND-COMPAT-001`, `INT-001`, `INT-005`
- Recorded implementation validation: CMD-01 passed 186 Node tests; CMD-03 passed 73 Python tests; CMD-04 passed 162 Python tests; `git diff --check` passed

## Actual-diff summary

- Added Node and Python lifecycle-contract classifiers with activation-manifest validation and shared classification fixtures.
- Added a tracked preactivation manifest and schema, permitted v2 in the change schema, and exposed classifier diagnostics from Node lifecycle readers.
- Preserved new-change compatibility by emitting explicit v1 draft metadata.
- Added focused Node and Python classifier tests, including manifest ordering, membership, vocabulary, and active-test-spec checks.
- Did not connect the Python classifier or activation manifest to the repository's production change-metadata and artifact-lifecycle validator entry points.

## Material findings

## Finding RTS-M1-CR1

Finding ID: RTS-M1-CR1
Severity: major
Location: `scripts/artifact_lifecycle_contracts.py:88`
Evidence: `classify_lifecycle_contract` reads `change.get("lifecycle_contract")`, checks unknown vocabulary only when the result is non-null, and then uses `explicit or LEGACY_UNVERSIONED_CONTRACT`. Consequently an explicitly present YAML/JSON null is classified as `legacy-unversioned`. A direct Python probe returned `{'contract_class': 'legacy-unversioned', 'activation_state': 'active', 'authority': 'prior-compatible'}` for `{'lifecycle_contract': None}`, while the corresponding Node classifier rejects null as `RL_UNSUPPORTED_SCHEMA: lifecycle_contract: unknown_value null`. This violates the required shared, deterministic classifier and the fail-closed unknown-contract rule in `RTS-R22`, `TS-002`, and the repository validator policy.
Required outcome: distinguish an absent lifecycle-contract key from an explicitly null value, reject explicit null as an unknown value before manifest consistency checks, and preserve Node/Python classification parity.
Safe resolution path: use key-presence or a sentinel in the Python classifier; add a named `unknown_value` explicit-null regression to the shared fixture or both focused suites; rerun CMD-01, CMD-03, and CMD-04.
needs-decision rationale: none; this is a bounded conformance correction under existing authority.

## Finding RTS-M1-CR2

Finding ID: RTS-M1-CR2
Severity: major
Location: `scripts/change_metadata_semantics.py:332`; `scripts/artifact_lifecycle_validation.py:1995`; `scripts/artifact_lifecycle_contracts.py:88`
Evidence: repository search finds `classify_lifecycle_contract`, `validate_lifecycle_activation_manifest`, and the activation manifest/schema path constants only at their definitions outside test files. `validate_stage_owned_lifecycle_metadata` recognizes v2 as vocabulary but returns immediately for every contract other than v1. The artifact-lifecycle validator invokes stage-owned semantics only when `lifecycle_contract` equals v1. A direct in-memory call through the production change-metadata validation path accepted a v2 record carrying active test-spec artifact and workflow state with no errors. The passing focused tests exercise the helper directly but do not prove that repository validators load the tracked manifest or enforce classification at their public boundary. This conflicts with the M1 plan requirement that the pure classifier be shared by runtime readers and repository validators and leaves `RTS-R18`, `RTS-R22`, `RTS-AC7`, `RTS-AC10`, `TS-001`, `TS-002`, and `TS-015` incomplete.
Required outcome: production repository validator paths must load and validate the tracked activation manifest, invoke the shared classifier for governed change records, reject inactive or contradictory v2/test-spec combinations, and enforce exact active-manifest membership and class matching for prior records.
Safe resolution path: integrate `artifact_lifecycle_contracts.py` through the existing change-metadata and artifact-lifecycle validator boundaries; add public-validator regressions for v2 with active test-spec state, prior-record missing or mismatched membership, and invalid manifest content while preserving preactivation v1 validity and inactive v2 behavior; rerun CMD-03 and CMD-04 plus CMD-01 for cross-runtime parity.
needs-decision rationale: none; this is the M1 integration boundary already approved by the plan.

## Checklist coverage

| Check | Result | Evidence |
|---|---|---|
| Spec alignment | block | The helper-level implementation covers most classification cases, but explicit null and production validator integration violate `RTS-R18` and `RTS-R22`. |
| Test coverage | block | Focused helper tests pass, but no public repository-validator regression proves that the classifier and tracked manifest govern actual validation. |
| Edge cases | block | Explicit null is silently reclassified as legacy-unversioned in Python. |
| Error handling | concern | Node fails closed for explicit null; Python does not. Other reviewed manifest vocabulary and ordering errors are specific. |
| Architecture boundaries | block | The approved classifier boundary is connected to Node readers but not repository validators. |
| Compatibility | concern | Prior-contract manifest constraints are not enforced through Python production validation, so bounded compatibility is not yet demonstrated. |
| Security/privacy | pass | No new secrets, credentials, external services, unsafe logging, or authorization data exposure were introduced. |
| Derived artifact currency | pass | M1's schema, manifest, and shared fixture are tracked; generated adapter publication remains allocated to a later milestone. |
| Unrelated changes | pass | The implementation paths are scoped to M1. The commit also contains the approved upstream lifecycle package because it is the branch's first commit; untracked `packages/rigorloop/node_modules/` is excluded from review. |
| Validation evidence | concern | The named suites passed, but their current coverage does not exercise the missing production integration and misses explicit-null parity. |

## No-finding rationale

Not applicable. Material findings `RTS-M1-CR1` and `RTS-M1-CR2` require resolution and rereview before M1 can close.

## Direct proof and residual risk

- Direct classification probes demonstrate the Node/Python explicit-null divergence.
- Static reachability inspection and a production-semantic probe demonstrate that Python public validators do not consume the new classifier or tracked manifest.
- The new-change path was also probed: its explicit v1 draft can still register the first artifact revision through the lifecycle context operation, so no additional workflow-dead-end finding was recorded.
- After these findings are corrected, rereview should focus on fail-closed ordering, manifest loading relative to repository roots, consistent error surfaces across both Python validators, and continued preactivation compatibility.

## Handoff

- Reviewed milestone: M1. Establish frozen contract classification and compatibility
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: resolve `RTS-M1-CR1` and `RTS-M1-CR2`, return M1 to implementation for the bounded corrections, rerun the exact M1 validation commands, and perform code-review again.
- Final closeout readiness: not ready; M1 has two open material findings and M2-M5 remain unstarted.
