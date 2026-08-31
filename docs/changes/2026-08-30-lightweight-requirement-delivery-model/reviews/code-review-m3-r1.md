# Code Review M3 R1: Package Parity and Holistic Publication Behavior

Review ID: code-review-m3-r1
Stage: code-review
Round: r1
Reviewer: Independent Codex code-review context
Reviewer authority: code-review
Review date: 2026-08-31
Target: M3 implementation commit `9c47498112c809885caaa5d4fe73fc76c31960ea` and workflow handoff commit `20d2f9107dd4c6823d3e0b1b95700daff1df4bca`
Reviewed milestone: M3
Reviewed artifact: M3 package-parity implementation at commit `9c47498112c809885caaa5d4fe73fc76c31960ea`, with holistic M1-M3 publication behavior
Status: changes-requested
Review status: changes-requested
Material findings: RTD-M3-CR1
Recording status: recorded

## Result

- Skill: code-review
- Status: completed
- Artifacts changed: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/code-review-m3-r1.md`, `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-log.md`, and `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-resolution.md`
- Open blockers: RTD-M3-CR1
- Next stage: review-resolution
- Review status: changes-requested
- Material findings: RTD-M3-CR1
- Recording status: recorded
- Recording blocker: none; no lifecycle transition is permitted until M3 has a clean review
- Review record: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/reviews/code-review-m3-r1.md`
- Review log: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-log.md`
- Review resolution: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/review-resolution.md`
- Reviewed milestone: M3
- Milestone closeout: resolution-needed
- Remaining implementation milestones: M3
- Required review-resolution: yes
- Finding IDs: RTD-M3-CR1
- Verify readiness: not-claimed

## Review inputs

- Exact M3 implementation: commit `9c47498112c809885caaa5d4fe73fc76c31960ea`
- Workflow handoff: commit `20d2f9107dd4c6823d3e0b1b95700daff1df4bca`
- Approved Design package: `design-review-r2`, members `architecture` and `spec`
- Approved Delivery package: `delivery-review-r2`, members `plan` and `test-spec`
- M3 allocation: RTD-R13-RTD-R14 and RTD-R17-RTD-R20; BND-COMPOSE-001, BND-RECOVERY-001, BND-COMPAT-001, BND-ENV-001; INT-002
- M3 tests: RTD-T07 and RTD-T08
- Implementation evidence: `docs/changes/2026-08-30-lightweight-requirement-delivery-model/evidence/m3-package-parity.md`
- Prior clean milestone evidence: `reviews/code-review-m1-r2.md` and `reviews/code-review-m2-r1.md`

## Actual-diff and holistic summary

M3 adds one canonical-source-to-local-copy byte comparison for the nine selected consumers, invokes it from canonical skill validation, and adds two focused tests plus milestone evidence. The prior M1 and M2 commits provide all nine byte-identical local references, their conditional resource-map entries, and stage-local responsibility text. Existing build, adapter archive, and clean-install code generically enumerates mapped resources, so the complete current package reaches temporary generated trees and all supported adapter installations without adding a publication mechanism or committed derived output.

The implementation correctly limits the new canonical comparison to authored canonical skills. Generated and installed trees continue through their existing structural and mapped-resource validators and are compared to canonical local skill packages, rather than attempting to resolve the repository-only shared template from customer installations. The selected-consumer set is a scoped applicability set rather than an input vocabulary: returning no issue for unrelated skills is intentional and documented by the helper's selected-consumer contract. No new lifecycle state, CLI operation, schema, archive manifest, or historical rewrite is present.

## Finding RTD-M3-CR1

Finding ID: RTD-M3-CR1
Severity: major
Location: `scripts/test-skill-validator.py:8880-8898`, with the production integration at `scripts/skill_validation.py:3722-3723`
Evidence: RTD-T07 requires the existing shared-resource, skill-build, and resource-map validation paths to be run over missing and altered variants, and the test specification explicitly says tests claiming package behavior must exercise existing public validator/build entrypoints rather than helper-only functions. The only new negative regression calls `validate_requirement_delivery_model_copy` directly. It never invokes `validate_skill_file`, `validate_skill_tree`, or `scripts/validate-skills.py`. Removing the production call at lines 3722-3723 leaves both new focused tests green: the positive test also calls the helper directly and compares bytes itself, while the negative test bypasses the integration point. The full current suite therefore proves the helper and the valid repository state but does not protect the M3 behavior that canonical skill validation actually fails closed on a drifted selected consumer.
Required outcome: Add a focused negative regression that drives a missing or drifted selected-consumer copy through the public skill-validation path and asserts the actionable diagnostic. Keep the helper-level assertion only if useful, and preserve the existing canonical-only scope so generated and installed validation continues through the correct generic package owners.
Safe resolution path: Build a temporary valid selected-skill fixture, point the validator's canonical-skill and shared-source roots at that fixture using test-local patching, mutate or remove its mapped requirement-to-delivery reference, and invoke `validate_skill_tree` or the existing validation CLI entrypoint. Assert the exact owning path diagnostic, demonstrate that removing the production integration call fails the regression, rerun CMD-001, CMD-003, CMD-004, and CMD-005, update M3 evidence, and request independent M3 rereview. Do not alter the approved model, package pipeline, generated outputs, or lifecycle schema.
needs-decision rationale: The implementation owner must record whether this bounded regression correction is accepted, rejected, deferred, or partially accepted; Code Review does not choose the disposition.

## Checklist coverage

| Item | Result | Evidence |
| --- | --- | --- |
| Spec alignment | concern | The production helper and package flow implement RTD-R13, RTD-R14, and RTD-R17-RTD-R20, but the required fail-closed validator integration proof is incomplete. |
| Test coverage | concern | Current valid-state, helper-negative, generated, archive, and clean-install checks pass; no regression exercises the new helper through the public skill-validator integration point. |
| Edge cases | concern | Missing and drifted helper cases are covered, and generic resource-map tests cover escaped and unmapped paths, but the selected-consumer integration can be disconnected without a test failure. |
| Error handling | pass in implementation | Missing canonical, missing local, and drifted local references return explicit path diagnostics; the gap is regression wiring rather than production error shape. |
| Architecture boundaries | pass | Canonical copy parity stays in existing skill validation; generated/archive/install parity stays with existing generic package owners. |
| Compatibility | pass | Historical artifacts, lifecycle state, review authority, test-spec ownership, and publication mechanisms are unchanged. |
| Security/privacy | pass | No credential, network, authorization, logging, persistence, or private-data surface changes. Existing path-containment checks remain active. |
| Derived artifact currency | pass for current state | Temporary generated output, all supported adapter archives, and clean installations validate; no derived skill body or archive is committed. |
| Unrelated changes | pass | M3 changes only the validator, focused tests, milestone evidence, and workflow handoff. The untracked `packages/rigorloop/node_modules/` tree is excluded. |
| Validation evidence | concern | All required commands pass, but passing proof does not detect removal of the new public-path integration call. |

## Validation rerun

- `python scripts/test-skill-validator.py -k RequirementDeliveryModelM3Tests` — passed, 2 tests.
- `python scripts/test-skill-validator.py` — passed, 368 tests.
- `python scripts/test-build-skills.py` — passed, 8 tests.
- `python scripts/build-skills.py --check` — passed using temporary output.
- `python scripts/test-adapter-distribution.py` — passed, 152 tests in 397.780 seconds; archive and clean-install checks exercise generic mapped-resource parity for supported adapters.
- `python scripts/validate-change-metadata.py docs/changes/2026-08-30-lightweight-requirement-delivery-model/change.yaml` — passed before review recording.
- `git diff --check 9c474981^ 20d2f910` — passed.

## Residual risk and handoff

The present implementation behaves correctly and the full current M1-M3 package is coherent, but the central M3 validator wiring can regress while every named test remains green. That proof gap is material because RTD-T07 and the approved M3 plan specifically authorize fail-closed integration, not only a callable helper.

This review is isolated and performs no implementation or lifecycle mutation. M3 remains `review-requested`, M4 must not start, and no automatic downstream handoff occurs. The exact next workflow action is review-resolution for RTD-M3-CR1, followed by a bounded M3 implementation correction and independent M3 rereview. The lifecycle CLI has no valid state-changing operation at this point; `complete-milestone` becomes the next workflow operation only after a clean M3 review receipt exists.
