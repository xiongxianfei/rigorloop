# Code Review M1 R1: Inactive V3 Lifecycle Classification

Review ID: code-review-m1-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review agent
Target: M1. Establish frozen v3 classification and compatibility
Reviewed artifact: commit `d5f9a85a` against baseline `f4cc4570`
Review date: 2026-09-01
Status: changes-requested
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m1-r1.md`, `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`, and `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Open blockers: `FV-M1-CR1`, `FV-M1-CR2`
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: `FV-M1-CR1`, `FV-M1-CR2`
- Recording status: recorded
- Recording blocker: none
- Review record: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/reviews/code-review-m1-r1.md`
- Review log: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-log.md`
- Review resolution: `docs/changes/2026-08-31-simplify-final-verification-retire-explain-change/review-resolution.md`
- Reviewed milestone: M1. Establish frozen v3 classification and compatibility
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Finding IDs: `FV-M1-CR1`, `FV-M1-CR2`
- Verify readiness: not-claimed

## Scope and authority

Reviewed the exact `f4cc4570..d5f9a85a` implementation diff against approved Design Review `design-review-r1`, approved Delivery Review `delivery-review-r1`, FV-R4 through FV-R7, FV-R28, FV-R31 through FV-R35, FV-R37, FV-R38, M1 TG-01 through TG-04, and the mapped state, temporal, recovery, compatibility, and interaction boundaries. The review also inspected implementation evidence `evidence/m1-v3-classification.md`, lifecycle schemas, Node and Python classifiers, public validator integration, fixtures, and scoped validation results.

The tracked governing state is exact and current: M1 is `review-requested`, Design and Delivery package authority is granted, the implementation commit is branch HEAD, and M2-M5 remain planned. This review is isolated and does not modify implementation, approved artifacts, milestone state, or workflow routing.

## Actual-diff summary

- Added `stage-owned-change-local-v3` as a recognized but preactivation contract in Node and Python.
- Added the tracked final-verification activation manifest, its schema, closed validation, exact v2 compatibility classification, and v3 active-explain-change rejection.
- Integrated the second manifest into runtime reading, change metadata validation, artifact lifecycle validation, and the governed lifecycle validator.
- Left v3 stage transitions, artifact kinds, and correction order empty while the tracked manifest remains preactivation; existing v2 creation and routing remain active.
- Added focused Node and Python tests plus implementation evidence and lifecycle handoff receipts.

## Material findings

## Finding FV-M1-CR1

Finding ID: FV-M1-CR1
Severity: major
Location: `scripts/validate-governed-lifecycle-cli.py:81-86`, `scripts/validate-governed-lifecycle-cli.py:101-112`, and `scripts/validate-governed-lifecycle-cli.py:150-154`
Evidence: The production inventory validator identifies governed contracts with raw substring tests such as `if f"lifecycle_contract: {LIFECYCLE_CONTRACT_V2}" in path.read_text(...)` instead of parsing the YAML value. A schema-valid record containing `lifecycle_contract: "stage-owned-change-local-v2"` is therefore omitted from `actual_v2`. A direct temporary-repository probe with that quoted value and an active empty final-verification manifest returned `[]` from `final_verification_manifest_errors`, meaning the wrapper approved an inventory that did not bind the v2 change. The Node classifier read the same semantic value and rejected the unlisted record with `RL_INCOMPATIBLE_VERSION`. Comments or unrelated scalar content containing the unquoted substring can produce the inverse false classification. This violates FV-R5's exact v2 binding, FV-R6's fail-closed mismatch rule, M1 TG-01/TG-03, BND-COMPAT-001, and the required Node/Python production-boundary parity.
Required outcome: Inventory and governed-record discovery must derive the lifecycle contract from parsed metadata with explicit key-presence and closed-vocabulary handling, so all schema-valid serializations classify identically and comments or unrelated text cannot select a contract.
Safe resolution path: Reuse the existing safe YAML loader and shared classifier rather than scanning raw text; build `actual_v2` and the v1/unversioned inventory from parsed semantic values; add public-wrapper regressions for quoted v2/v3 values, a misleading comment or unrelated scalar, exact missing membership, and unchanged ordinary records; rerun all four M1 command groups and the governed wrapper.
needs-decision rationale: none; this is a bounded conformance correction under the approved M1 contract.

## Finding FV-M1-CR2

Finding ID: FV-M1-CR2
Severity: minor
Location: `packages/rigorloop/test/lifecycle-contract.test.js:32-83`, `scripts/test-change-metadata-validator.py:2339-2399`, and `scripts/test-artifact-lifecycle-validator.py:5370-5381`
Evidence: M1 TG-02 explicitly requires direct rejection of duplicate and unsorted entries in the new final-verification manifest, and the implementation evidence claims those tests were added. Repository search finds no test that mutates the new final-verification manifest into duplicate or unsorted states. Existing duplicate/order tests exercise only the older lifecycle activation validator. The new Node and Python functions contain ordering checks, but code shape is not direct proof for the named compatibility boundary. The four planned suites pass because this new-manifest edge is absent from their test inputs.
Required outcome: The new final-verification manifest's duplicate and raw-UTF-8 ordering behavior must have direct Node and Python regression proof, including fail-closed error ordering where an unknown closed value is also present.
Safe resolution path: Add named duplicate and unsorted cases against `validateFinalVerificationActivationManifest` and `validate_final_verification_activation_manifest`, plus a public validator case proving malformed final-manifest ordering blocks activation; rerun the M1 Node, change-metadata, artifact-lifecycle, and governed-wrapper suites.
needs-decision rationale: none; this completes proof already required by M1 TG-02 without changing behavior or scope.

## Checklist coverage

| Check | Result | Evidence |
| --- | --- | --- |
| Spec alignment | block | Core inactive-v3 behavior aligns, but raw-text inventory discovery does not provide FV-R5/FV-R6 exact semantic classification. |
| Test coverage | block | Planned suites pass, but the quoted-contract production counterexample and new-manifest duplicate/order cases are uncovered. |
| Edge cases | block | Quoted YAML scalars and misleading comments can change wrapper inventory classification; duplicate/order proof is missing for the new manifest. |
| Error handling | concern | Runtime and helper classifiers fail closed, but the wrapper can report a false-clean inventory for a valid quoted v2 value. |
| Architecture boundaries | concern | Node and Python shared classifier logic is substantially aligned, but the production wrapper bypasses it at record discovery and inventory construction. |
| Compatibility | block | Exact historical v2 binding is not guaranteed across valid YAML representations. |
| Security/privacy | pass | No secrets, credentials, external calls, private environment capture, or new authority data exposure were introduced. |
| Derived artifact currency | pass | The new schema, tracked preactivation manifest, fixtures, and runtime/Python consumers are present; later skill and adapter output remains out of M1 scope. |
| Unrelated changes | pass | The diff is limited to M1 lifecycle classification, validation, tests, evidence, and required lifecycle receipts. |
| Validation evidence | concern | All planned suites and the current repository wrapper pass, but the direct counterexample demonstrates a production gap those suites do not detect. |

## Direct proof and residual risk

The following reviewer-run checks passed:

- `node --test packages/rigorloop/test/lifecycle-contract.test.js packages/rigorloop/test/lifecycle-read.test.js packages/rigorloop/test/lifecycle-stage-advance.test.js` — 70 tests passed.
- `python scripts/test-change-metadata-validator.py` — 86 tests passed.
- `python scripts/test-artifact-lifecycle-validator.py` — 167 tests passed.
- `python scripts/test-governed-lifecycle-cli-validator.py` — 10 tests passed.
- `python scripts/validate-governed-lifecycle-cli.py` — passed for 34 records with the two approved baseline warnings.
- `git diff --check f4cc4570 d5f9a85a` — passed.

A direct temporary-repository probe then demonstrated FV-M1-CR1: the wrapper returned no final-verification inventory error for an unlisted quoted v2 contract, while the Node semantic classifier rejected the same unlisted v2 identity. No implementation was changed during the probe.

Beyond the findings, the reviewed implementation correctly keeps the tracked final-verification manifest preactivation, leaves v3 with no transitions, artifact inventory, or correction stages, preserves current v2 authority and route tests, rejects active explain-change state in v3 classifiers and metadata semantics, and avoids adding any Verify report writer or self-referential report identity in M1.

## Handoff

- Reviewed milestone: M1. Establish frozen v3 classification and compatibility
- Review status: changes-requested
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M1, M2, M3, M4, M5
- Required review-resolution: yes
- Recommended next stage: record accepted dispositions for `FV-M1-CR1` and `FV-M1-CR2`, return M1 to implementation for bounded correction, rerun the exact M1 commands, and perform Code Review M1 R2 over every changed implementation file.
- Final closeout readiness: not ready; M1 has two open material findings and M2-M5 remain unstarted.
